import json, boto3

def lambda_handler(event, context):
    bedrock_client = boto3.client('bedrock-runtime')
    
    # get the user prompt
    prompt = event['prompt']

    # invoke the model
    response = bedrock_client.invoke_model(
        modelId='cohere.command-light-text-v14',
        body=json.dumps(
            {
               "prompt": prompt,
               "max_tokens": 100,
               "temperature": 0.9,
               "p": 0.75,
               "k": 0    
            }
        ),
        contentType='application/json',
        accept='application/json'
    )

    # get the response from the model
    response_body = json.loads(response.get('body').read())
   
    return {
        'statusCode': 200,
        'body': response_body['generations'][0]['text']
    }
