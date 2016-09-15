###A Custom Provisioner for configuring S3 Bucket Transfer Acceleration

A provisioner for setting the S3 Bucket Accelerate Configuration Policy as part of a CloudFormation stack. 
Currently this attribute is not available within CloudFormation standard resources.


#### Provisioning the Provisioner

Generate the template:
`make all`

Upload it to CloudFormation:
`make deploy`


#### Using the Provisioner in another stack

A simple Node.js provisioner that runs in AWS Lambda. This stack can be used to add S3 Bucket Acceleration policies
to S3 buckets created as part of Cloudformation stacks.

To set the Bucket Accelerate Policy as part of a Cloudformation Stack, an AWS Custom Object is used.

In Python, you can create the custom object with Troposphere

```
from troposphere.cloudformation import AWSCustomObject


class BucketAccelerateConfiguration(AWSCustomObject):
    resource_type = "Custom::CloudwatchEvent"
    props = {
        'ServiceToken': (basestring, True),
        'Status': (basestring, True),
        'Bucket': (basestring, True)
    }

```

You then simply need to instantiate the custom CloudFormation resource and add it to your template
```
from troposphere import Template, Ref
from troposphere.s3 import Bucket, PublicRead


t = Template()
s3bucket = Bucket(
    "MyS3Bucket",
    AccessControl=PublicRead
)
t.add_resource(s3bucket)

accelerate_configuration = BucketAccelerateConfiguration(
    "MyS3AccelerateConfiguration",
    ServiceToken='MyProvisionerLambdaFunctionArn',
    Status='Enabled',
    Bucket=Ref(s3bucket)
)
t.add_resource(accelerate_configuration)

```

ServiceToken: the ARN of the Lambda function provisioned by the stack created by this project
Status: 'Enabled' or 'Suspended'
Bucket: The S3 Bucket for which you are creating the policy. We pass a reference to the bucket, since we're creating it
in the same stack