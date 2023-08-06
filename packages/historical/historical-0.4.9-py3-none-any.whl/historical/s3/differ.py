"""
.. module: historical.s3.differ
    :platform: Unix
    :copyright: (c) 2017 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. author:: Mike Grima <mgrima@netflix.com>
"""
import logging

from raven_python_lambda import RavenLambdaWrapper

from historical.common.util import deserialize_records
from historical.constants import LOGGING_LEVEL
from historical.s3.models import CurrentS3Model, DurableS3Model
from historical.common.dynamodb import process_dynamodb_differ_record

logging.basicConfig()
LOG = logging.getLogger('historical')
LOG.setLevel(LOGGING_LEVEL)

# Path to where in the dict the ephemeral field is -- starting with "root['M'][PathInConfigDontForgetDataType]..."
# EPHEMERAL_PATHS = []


@RavenLambdaWrapper()
def handler(event, context):  # pylint: disable=W0613
    """
    Historical S3 event differ.

    Listens to the Historical current table and determines if there are differences that need to be persisted in the
    historical record.
    """
    # De-serialize the records:
    records = deserialize_records(event['Records'])

    for record in records:
        process_dynamodb_differ_record(record, CurrentS3Model, DurableS3Model)
