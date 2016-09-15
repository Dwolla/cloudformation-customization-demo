from troposphere import Join, GetAtt
from troposphere.awslambda import Function, Code
import boto3


def make_alphanumeric(the_string):
    return ''.join(e for e in the_string if e.isalnum())


def lambda_source_code(source_filename):
    with open(source_filename, 'r') as f:
        code = f.read()
    return code


class LambdaFunction(Function):
    def __init__(self, role, lambda_config, project):
        function_name = '%sFunction' % project
        code = lambda_config.get('code')
        super(LambdaFunction, self).__init__(
            function_name,
            Code=Code(ZipFile=Join('\n', code.split('\n'))),
            Handler=lambda_config['handler'],
            Role=GetAtt(role, "Arn"),
            Runtime=lambda_config['runtime'],
            MemorySize=lambda_config['memory'],
            Timeout=lambda_config['timeout']
        )
