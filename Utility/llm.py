from langchain_openai import AzureChatOpenAI

import os
from dotenv import load_dotenv

load_dotenv()



# Your Azure OpenAI setup
llm = AzureChatOpenAI(
            api_key= os.getenv("AZURE_OPENAI_KEY") ,
            azure_endpoint= os.getenv("AZURE_OPENAI_ENDPOINT"),
            openai_api_version="2024-02-01",  # Ensure this matches your Azure API version
            model="gpt-4o",
            deployment_name= os.getenv("AZURE_OPENAI_MODEL"),
            temperature=0,
            verbose = True
)