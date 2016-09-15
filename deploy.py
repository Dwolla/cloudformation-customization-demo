import boto3

with open('target/provisioner_stack.json') as f:
    template_json = f.read()

print(template_json)

cloudformation = boto3.client('cloudformation')
print("Creating Cloudformation Stack")
cloudformation.create_stack(
    StackName='S3AccelerationProvisioner',
    TemplateBody=template_json,
    Capabilities=['CAPABILITY_IAM']
)
