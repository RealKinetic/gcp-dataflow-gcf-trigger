# gcp-dataflow-gcf-trigger

Trigger a Dataflow job when a file is uploaded to Cloud Storage using a Cloud
Function. This works by launching pre-configured Dataflow templates. This can
be used to trigger Dataprep flows from Cloud Storage (or other) events.

For triggering Dataprep flows using the Dataprep API rather than Dataflow, see
[gcp-dataprep-gcf-trigger](https://github.com/RealKinetic/gcp-dataprep-gcf-trigger).

## Deploying

Run the following command to deploy this Cloud Function:

```
$ gcloud functions deploy <function-name> \
    --entry-point trigger \
    --trigger-bucket gs://<my-bucket> \
    --set-env-vars DATAFLOW_TEMPLATE=<dataflow-template-gcs-path>,BIGQUERY_DATASET=<bigquery-output-dataset>,BIGQUERY_TABLE=<bigquery-output-table>,TEMP_LOCATION=<temp-output-gcs-path> \
    --runtime python37
```

This function assumes a Dataflow template with a single input and output
location, i.e. a Dataprep template.

## Environment Variables

As shown above, this Cloud Function requires four environment variables:

- `DATAFLOW_TEMPLATE`: GCS path for Dataflow template
- `BIGQUERY_DATASET`: BigQuery dataset for output
- `BIGQUERY_TABLE`: BigQuery table for output
- `TEMP_LOCATION`: GCS path for temporary output
