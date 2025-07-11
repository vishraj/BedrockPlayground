from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from langchain_aws import ChatBedrockConverse
import boto3

def demo_chatbot():
    session = boto3.Session(profile_name="156041445517_AWSAdministratorAccess")
    bedrock_client=session.client("bedrock-runtime", region_name="us-east-1")
    demo_llm = ChatBedrockConverse(
        client=bedrock_client,
        model="cohere.command-r-v1:0",
        max_tokens=1000,
        temperature=0.1)
    
    return demo_llm

# create the function for the conversation buffer memory
def demo_memory():
    llm_data = demo_chatbot()
    memory = ConversationSummaryBufferMemory(llm=llm_data, max_token_limit=2000)
    return memory

# create the function for the langchain conversation chain
def demo_conversation(input_text, memory):
    llm_data = demo_chatbot()
    conversation = ConversationChain(llm=llm_data, memory=memory, verbose=True)

    # chat reponse using invoke
    chat_reply = conversation.invoke(input_text)
    
    return chat_reply['response']



