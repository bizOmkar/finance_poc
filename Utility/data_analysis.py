import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents import AgentType
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate

from prompts.Prompt_data_analysis import system_instruction



def analyze_data(query, llm, df_ebitda_walk_impact, df_ytd):
    
    full_query = f"{system_instruction}\n\nUser Query: {query}"
    print("*********************************************************")
    print("system_instruction, df_ebitda_walk_impact, df_ytd and query received for analysis ")
    print("*********************************************************")
    
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=[df_ebitda_walk_impact, df_ytd],
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        # handle_parsing_errors=True,
        allow_dangerous_code=True
    )
     

    response = agent.invoke(full_query)
    if response:
        print("*********************************************************") 
        print(f"response: {response}")
    else:
        print("No response received from the agent.")
    return response["output"]
