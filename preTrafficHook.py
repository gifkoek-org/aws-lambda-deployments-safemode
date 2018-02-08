import boto3
import os
import json


# the codedeploy and lambda objects
cd = boto3.client("codedeploy")
lambda_client = boto3.client("lambda")
# the name and version of the newly deployed Lambda to test
# the "CurrentVersion" environment variable is set up by the samTemplate
lambda_to_test = os.environ["CurrentVersion"]


def lambda_handler(event, context):
    """
    returns a 200
    """
    deployment_id = event["DeploymentId"]
    lifecycle_event_hook_execution_id = event["LifecycleEventHookExecutionId"]

    # invoke the specific Lambda to test
    function_details = lambda_to_test.split(":")     # list with name and version in elements 0 & 1
    response = lambda_client.invoke(
        FunctionName=function_details[0],            # function name
        InvocationType="RequestResponse",
        Qualifier=function_details[1]                # function version
    )

    print(json.dumps(response, indent=4))            # debug print
    if "StatusCode" in response:
        if response["StatusCode"] == 200:
            test_status = "Succeeded"
        else:
            test_status = "Failed"

    # Prepare the validation test results with the deploymentId and
    # the lifecycleEventHookExecutionId for AWS CodeDeploy.
    params = {"deploymentId": deployment_id,
              "lifecycleEventHookExecutionId": lifecycle_event_hook_execution_id,
              "status": test_status
    }

# Pass AWS CodeDeploy the prepared validation test results.
    response = cd.put_lifecycle_event_hook_execution_status(
        deploymentId=deployment_id,
        lifecycleEventHookExecutionId=lifecycle_event_hook_execution_id,
        status="Succeeded"
    )

"""
{
if (err)
{
// Validation
failed. \
    console.log('Validation test failed');
console.log(err);
console.log(data);
callback('Validation test failed');
} else {
       // Validation
succeeded. \
    console.log('Validation test succeeded');
callback(null, 'Validation test succeeded');
}
});
}
"""