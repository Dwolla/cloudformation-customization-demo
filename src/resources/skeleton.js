var response = require('cfn-response');

exports.handler = function(event, context, callback) {
    var ResourceProperties = event.ResourceProperties;
    var responseData = {};
    if (event.ResourceType == 'Create') {
        //API call for Create
    } else if (event.ResourceType == 'Update') {
        //API call for Update
    } else if (event.ResourceType == 'Delete') {
        //API call for Delete
    }
    response.send(event, context, response.SUCCESS, responseData);
};