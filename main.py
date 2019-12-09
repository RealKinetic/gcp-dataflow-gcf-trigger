import json
import os
import random
import string

import googleapiclient.discovery


PROJECT_ID = os.getenv('GCP_PROJECT')
DATAFLOW_TEMPLATE = os.getenv('DATAFLOW_TEMPLATE')
FUNCTION_NAME = os.getenv('FUNCTION_NAME')
BIGQUERY_DATASET = os.getenv('BIGQUERY_DATASET')
BIGQUERY_TABLE = os.getenv('BIGQUERY_TABLE')
TEMP_LOCATION = os.getenv('TEMP_LOCATION')


dataflow = googleapiclient.discovery.build('dataflow', 'v1b3',
                                           cache_discovery=False)


def trigger(event, context):
    """Triggered by a change to a Cloud Storage bucket. This will launch a
    Dataflow job based on the configured template for files uploaded to Cloud
    Storage.

    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    # Generate a job name based on the Cloud Function name and a random ID.
    job_id = ''.join(random.choice(string.ascii_lowercase +
                                   string.digits) for _ in range(8))
    job_name = '{}-{}'.format(FUNCTION_NAME, job_id).lower()

    # Configure input and output locations.
    input_file = 'gs://{}/{}'.format(event['bucket'], event['name'])
    input_locations = {'location1': input_file}
    output_locations = {'location1': '{}:{}.{}'.format(
        PROJECT_ID, BIGQUERY_DATASET, BIGQUERY_TABLE)}

    # Start the Dataflow job.
    print("Launching Dataflow job for template '{}'".format(DATAFLOW_TEMPLATE))
    result = dataflow.projects().templates().launch(
        projectId=PROJECT_ID,
        body={
            "parameters": {
                "inputLocations": json.dumps(input_locations),
                "outputLocations": json.dumps(output_locations),
                "customGcsTempLocation": TEMP_LOCATION,
            },
            "jobName": job_name
        },
        gcsPath=DATAFLOW_TEMPLATE
    ).execute()

    job = result['job']
    print("Dataflow job '{}' created".format(job['name']))

