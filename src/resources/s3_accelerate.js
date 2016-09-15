var response = require('cfn-response');

exports.handler = function(event, context, callback) {
    console.log('REQUEST RECEIVED:\n', JSON.stringify(event));
    var accelerateStatus = event.ResourceProperties.Status;
    var s3bucket = event.ResourceProperties.Bucket;

    var responseData = {};

    if (!s3bucket || !accelerateStatus) {
        responseData.Message = "Missing required parameter 'Bucket' or 'Status'";
        response.send(event, context, response.FAILED, responseData);
    }

    var AWS = require('aws-sdk');
    var s3 = new AWS.S3();
    //s3.putBucketAccelerateConfiguration(newparams, function (err, data) {

    if (event.RequestType == 'Create' || event.RequestType == 'Update') {
        var params = {
            Bucket: s3bucket,
            AccelerateConfiguration: {Status: AccelerateStatus}
        }
        s3.putBucketAccelerateConfiguration(params, function (err, data) {
            if (err) {
                console.log(err, err.stack);
                responseData['Message'] = err;
                response.send(event, context, response.FAILED, responseData);
            } else {
                responseData.Message = 'Successfully Updated Bucket Accelerate Configuration'
                response.send(event, context, response.SUCCESS, responseData);
            }
        });
    } else if (event.RequestType == 'Delete') {
        responseData.Message = 'Success';
        response.send(event, context, response.SUCCESS, responseData);
    } else {
        responseData.Message = "Did not understarnd RequestType. Must be Create, Update, or Delete";
        response.send(event, context, response.FAILED, responseData);
    }
};