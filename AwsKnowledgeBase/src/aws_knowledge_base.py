import json
import boto3
from botocore.exceptions import ClientError

# Create a client connection with bedrock
# Lambda will use the execution role's permissions
client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

def lambda_handler(event, context):
    try:
        user_prompt = event.get('prompt', '')
        if not user_prompt:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No prompt provided'})
            }
            
        # use the retrieve and generate API
        response = client.retrieve_and_generate(
            input={
                'text': user_prompt
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': '0MBGIQ7JSK',
                    'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'
                }
            }
        )

        answer_text = response['output']['text']
        
        return {
            'statusCode': 200,
            'body': answer_text
        }
    except ClientError as e:
        print(f"Bedrock API error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Error calling Bedrock: {str(e)}"})
        }
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Unexpected error: {str(e)}"})
        }