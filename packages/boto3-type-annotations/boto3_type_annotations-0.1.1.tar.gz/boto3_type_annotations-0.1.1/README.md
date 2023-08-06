# boto3_type_annotations

A programmatically created package that defines `boto3` services as dummy class with type annotations.

```python
import boto3
from boto3_type_annotations import sqs


client: sqs.Client = boto3.client('sqs')
resource: sqs.ServiceResource = boto3.resource()

client.send_message(QueueUrl='foo', MessageBody='bar')

queue = resource.Queue('foo')
queue.send_message(MessageBody='foo')

```