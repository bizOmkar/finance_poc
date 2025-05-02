from pandasai import Agent
import matplotlib.pyplot as plt
from Utility.dynamic_ebitda_walk import fig_to_base64



def run_ytd_analysis_plot(df_ytd, query, llm):
    print("*********************************************************")
    print(" query, df_ytd received for plotting")
    print("*********************************************************")

    try:
        agent = Agent(df_ytd, config={
            "llm": llm,
            "cache": None,
            "verbose": True
        })

        result = agent.chat(query)

        if result:
            print("*********************************************************") 
            print(f"result: {result}")
        else:
            print("No result received from the plot agent.")
            return {"type": "text", "data": "No result received from the agent."}

        if isinstance(result, plt.Figure):
            print("Plot Generated Successfully")
            return {"type": "image", "data": fig_to_base64(result)}
        else:
            return {"type": "text", "data": result}

    except Exception as e:
        print("Error during YTD analysis and plotting:", str(e))
        return {"type": "text", "data": "Failed to analyze or generate plot due to an error."}
