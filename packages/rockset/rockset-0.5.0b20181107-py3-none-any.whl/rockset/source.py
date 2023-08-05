"""
Introduction
------------
Source objects represent various data sources that could be used to create
collections.

Example usage
-------------
::

    from rockset import Client, Q, F
    import os

    rs = Client()

    # create a collection from an AWS S3 bucket
    integration = rs.Integration.retrieve('aws-rockset-read-only')
    s3 = rs.Source.s3(bucket='my-s3-bucket',
        integration=integration)
    newcoll = rs.Collection.create(name='newcoll', sources=[s3])

Create AWS S3 source for a collection
-------------------------------------
AWS S3 buckets can be used as a data source for collections::

    from rockset import Client, Q, F
    import os

    rs = Client()

    # create a collection from an AWS S3 bucket
    integration = rs.Integration.retrieve('aws-rockset-read-only')
    s3 = rs.Source.s3(bucket='my-s3-bucket',
        integration=integration)
    newcoll = rs.Collection.create(name='newcoll', sources=[s3])

.. automethod :: rockset.Source.s3

"""

import csv

from rockset.integration import Integration

from rockset.query import FieldRef


class Source(object):
    def __str__(self):
        return str(vars(self))

    def __iter__(self):
        for k, v in vars(self).items():
            yield (k, v)

    @classmethod
    def s3(
        cls,
        bucket,
        prefixes=None,
        integration=None,
        data_format=None,
        csv_params=None
    ):
        """ Creates a source object to represent an AWS S3 bucket as a
        data source for a collection.

        Args:
            bucket (str): Name of the S3 bucket
            prefixes (list of str): Path prefix to only source S3 objects that
                are recursively within the given path. (optional)
            integration (rockset.integration.Integration): An Integration object (optional)
            data_format (str): oneof "json", "parquet, "xml" or "csv"
                [default: "auto_detect"]
            csv_params (CsvParams): if CSV, then specifications of the CSV format
        """
        return SpecificSource(
            bucket=bucket,
            prefixes=prefixes,
            integration=integration,
            data_format=data_format,
            csv_params=csv_params
        )

    @classmethod
    def dynamo(
        cls,
        table_name,
        integration=None,
        data_format=None,
        csv_params=None
    ):
        """ Creates a source object to represent an AWS DynamoDB table as a
        data source for a collection.

        Args:
            table_name (str): Name of the DynamoDb table
            integration (rockset.integration.Integration): An Integration object (optional)
            data_format (str): oneof "json", "parquet, "xml" or "csv"
                [default: "auto_detect"]
            csv_params (CsvParams): if CSV, then specifications of the CSV format
        """
        return SpecificSource(
            table_name=table_name,
            integration=integration,
            data_format=data_format,
            csv_params=csv_params
        )

    @classmethod
    def kinesis(cls,
                stream_name,
                integration,
    ):
        """ Created a source object to represent a Kinesis Stream as a
        data source for a collection

        Args:
            stream_name (str): Name of the Kinesis Stream
            integration (rockset.integration.Integration): An Integration object (optional)
        """

        return SpecificSource(
            stream_name=stream_name,
            integration=integration
        )

    @classmethod
    def csv_params(
        cls,
        separator=None,
        encoding=None,
        first_line_as_column_names=None,
        column_names=None,
        column_types=None
    ):
        """ Creates a object to represent options needed to parse a CSV file

        Args:
            separator (str): The separator between column values in a line
            encoding (str): The encoding format of data, one of "UTF-8",
                "UTF-16" "US_ASCII"
                [default: "US-ASCII"]
            first_line_as_column_names (boolean): Set to true if the first line
                of a data object has the names of columns to be used. If this is
                set to false, the the column names are auto generated.
                [default: False]
            column_names (list of strings): The names of columns
            column_types (list of strings): The types of columns
        """
        return CsvParams(
            separator=separator,
            encoding=encoding,
            first_line_as_column_names=first_line_as_column_names,
            column_names=column_names,
            column_types=column_types
        )


class SpecificSource(Source):
    def __init__(
        self,
        bucket=None,
        prefixes=None,
        table_name=None,
        stream_name=None,
        integration=None,
        data_format=None,
        csv_params=None
    ):
        if isinstance(integration, Integration):
            self.integration_name = integration.name
        elif integration is not None:
            ret = 'TypeError: invalid object type {} for integration'.format(
                type(integration)
            )
            raise TypeError(ret)

        # If this is a S3 source, then fill up S3 specificatins
        if bucket is not None:
            self.s3 = {
                'format': data_format,
                'bucket': bucket,
            }
            if prefixes is not None:
                self.s3['prefixes'] = prefixes

        # If this is a DynamoDB source, then fill up table specificatins
        if table_name is not None:
            self.dynamodb = {
                'table_name': table_name,
            }

        # If this is a kinesis source, then fill up stream specifications
        if stream_name is not None:
            self.kinesis = {
                'stream_name': stream_name,
            }

        if data_format is not None:
            self.format = data_format

        self.format_params_csv = {
            'firstLineAsColumnNames': False,
            'separator': ",",
            'encoding': "US-ASCII",
            'columnNames': [],
        }
        if csv_params is not None:
            if csv_params.separator is not None:
                self.format_params_csv['separator'] = csv_params.separator
            if csv_params.encoding is not None:
                self.format_params_csv['encoding'] = csv_params.encoding
            if csv_params.first_line_as_column_names is not None:
                self.format_params_csv['firstLineAsColumnNames'
                                      ] = csv_params.first_line_as_column_names
            if csv_params.column_names is not None:
                if not isinstance(csv_params.column_names, list):
                    raise ValueError(
                        "column names of type {} "
                        "not supported".format(type(csv_params.column_names))
                    )
                self.format_params_csv['columnNames'] = csv_params.column_names
            if csv_params.column_types is not None:
                if not isinstance(csv_params.column_types, list):
                    raise ValueError(
                        "column types of type {} "
                        "not supported".format(type(csv_params.column_types))
                    )
                self.format_params_csv['columnTypes'] = csv_params.column_types


#
# Parameters needed for a CSV formatted data set
#
class CsvParams:
    def __init__(
        self, separator, encoding, first_line_as_column_names, column_names,
        column_types
    ):
        self.separator = separator
        self.encoding = encoding
        self.first_line_as_column_names = first_line_as_column_names
        self.column_names = column_names
        self.column_types = column_types
