from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Check if essential environment variables exist
    api_key = os.getenv("AZURE_OPENAI_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_MODEL")

    if not all([api_key, endpoint, deployment]):
        raise EnvironmentError("One or more required environment variables are missing.")

    llm = AzureChatOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        openai_api_version="2024-02-01",  # Ensure this matches your Azure API version
        model="gpt-4o",
        deployment_name=deployment,
        temperature=0,
        verbose=True
    )

except Exception as e:
    print("Error initializing AzureChatOpenAI:", str(e))
    llm = None  # Or raise error / exit depending on app design
