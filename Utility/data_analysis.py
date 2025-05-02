from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents import AgentType
from langchain.chat_models import AzureChatOpenAI

from prompts.Prompt_data_analysis import system_instruction

def analyze_data(query, llm, df_ebitda_walk_impact, df_ytd):
    try:
        full_query = f"{system_instruction}\n\nUser Query: {query}"
        print("*********************************************************")
        print("system_instruction, df_ebitda_walk_impact, df_ytd and query received for analysis")
        print("*********************************************************")
        
        try:
            agent = create_pandas_dataframe_agent(
                llm=llm,
                df=[df_ebitda_walk_impact, df_ytd],
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                allow_dangerous_code=True
            )
        except Exception as e:
            print("Error while creating the agent:", str(e))
            return {"output": f"Agent creation failed: {str(e)}"}

        try:
            response = agent.invoke(full_query)
            print("*********************************************************") 
            print(f"response: {response}")
            return response["output"]
        except Exception as e:
            print("Exception during agent invocation:", str(e))
            return {"output": f"Error occurred while processing the query: {str(e)}"}

    except Exception as e:
        print("Unexpected error in analyze_data function:", str(e))
        return {"output": "An unexpected error occurred during analysis."}
