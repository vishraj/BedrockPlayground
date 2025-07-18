import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.indexes import VectorstoreIndexCreator
from langchain_aws import ChatBedrock

def rag_index():
    # Load the document using pypdf
    pdf_path = os.path.join(os.path.dirname(__file__), "houn.pdf")
    data_load = PyPDFLoader(pdf_path)
    data_split = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", ".", " "],
                                                chunk_size=1000, 
                                                chunk_overlap=200)

    # create the embeddings
    data_embeddings = BedrockEmbeddings(credentials_profile_name="156041445517_AWSAdministratorAccess",
                                        model_id="amazon.titan-embed-text-v2:0",
                                        region_name="us-east-1")

    # create the vector db, store the embeddings and create an index for searching the document
    # VectorstoreIndexCreator is a wrapper that does all of the above
    data_index = VectorstoreIndexCreator(vectorstore_cls=FAISS,
                                        embedding=data_embeddings,
                                        text_splitter=data_split,
                                        )
    db_index = data_index.from_loaders([data_load])
    return db_index

# connect to the bedrock FM
def rag_llm():
    llm = ChatBedrock(
        credentials_profile_name="156041445517_AWSAdministratorAccess",
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        region_name="us-east-1",
        model_kwargs={
            "max_tokens": 2000,
            "temperature": 0.1,
            "top_p": 0.9
        }
    )    
    return llm

# This function takes a user prompt, searches the vector DB for the best match and sends both to the LLM
def rag_response(index, question):
    llm = rag_llm()
    response = index.query(question=question, llm=llm)
    return response





