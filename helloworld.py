"""
return a 200
"""


def lambda_handler(event, context):
    """
    returns a 200
    """
    return {
        "statusCode": "200",
        "body": "hello world",
        "headers": {
            "Content-Type": "application/json"
        }
    }