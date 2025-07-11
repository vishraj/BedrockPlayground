import json, boto3, base64, datetime

def lambda_handler(event, context):
    # 1. create a client connection for bedrock and s3
    bedrock_client = boto3.client('bedrock-runtime')
    s3_client = boto3.client('s3')

    # 2.store the prompt in a variable
    prompt = event['prompt']
    print(prompt)

    # 3. invoke the bedrock service
    response = bedrock_client.invoke_model(
        contentType='application/json',
        accept='application/json',
        modelId='stability.stable-diffusion-xl-v1',
        body=json.dumps({
            "text_prompts": [
                {
                    "text": prompt
                }
            ],
            "cfg_scale": 20,
            "seed": 0,
            "steps": 80
        })
    )

    # 4. retrieve the response, convert to bytes and decode from base64
    response_as_bytes = json.loads(response['body'].read())
    base64_image = response_as_bytes['artifacts'][0]['base64']
    final_image = base64.b64decode(base64_image)

    # 5. upload the file to s3 bucket
    poster_name = 'posterName' + datetime.datetime.today().strftime("%Y-%M-%D-%M-%S") + '.png'
    s3_client.put_object(Bucket='vr-movieposterdesign01', Key=poster_name, Body=final_image)

     # 6. generate the presigned url
    url = s3_client.generate_presigned_url('get_object', 
                                            Params={
                                                'Bucket': 'vr-movieposterdesign01', 
                                                'Key': poster_name
                                            }, ExpiresIn=3600)
    print(f"pre-signed url: {url}")

    return {
        'statusCode': 200,
        'body': url
    }