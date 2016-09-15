from os import path
from troposphere import Template, Output, GetAtt
from resources.helpers import lambda_source_code, LambdaFunction
from resources.iam import S3AccelerateProvisionerRole


code_file = path.join(path.dirname(__file__), 'resources', 's3_accelerate.js')
provisioner_config = {
    'code': lambda_source_code(code_file),
    'runtime': 'nodejs',
    'handler': 'index.handler',
    'timeout': 30,
    'memory': 128
}

t = Template()
t.add_description('Lambda stack for provisioning S3 Bucket Acceleration Policies')

provisioner_role = S3AccelerateProvisionerRole()
t.add_resource(provisioner_role)

provisioner_function = LambdaFunction(provisioner_role, provisioner_config, 'LambdaS3AccelerationProvisioner')
t.add_resource(provisioner_function)

output = Output("FunctionArn", Value=GetAtt(provisioner_function, "Arn"))
t.add_output(output)

print(t.to_json())
