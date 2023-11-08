# aws-recipes-analytics

EC2InstanceKinesisAgent: 

Runs EC2 instance with installed and configured kinesis agent.

Kinesis agent reads logs from the specified directory (see #file in Metadata)

A python app write the logs in the same directory.


FirehoseDStoS3:

Creates a firehose delivery stream.

Writes in S3 bucket.

Creates roles and policies to write in S3 and cloudwatch groups





The `stock` generated data sample is the same that [pyflink-getting-started](https://github.com/aws-samples/pyflink-getting-started)