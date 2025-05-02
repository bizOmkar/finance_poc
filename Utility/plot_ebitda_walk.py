from pandasai import Agent
import matplotlib.pyplot as plt

from prompts.Prompt_plot_ebitda_walk import system_prompt
from Utility.dynamic_ebitda_walk import fig_to_base64

import matplotlib
matplotlib.use('Agg')

def run_ebitda_walk_analysis_plot(df_ebitda_walk_impact, query, llm):
    print("*********************************************************")
    print("system_prompt, query, df_ebitda_walk_impact received for plotting")
    print("*********************************************************")

    try:
        agent = Agent(
            df_ebitda_walk_impact,
            config={
                "llm": llm,
                "cache": None,
                "verbose": True,
                "system_prompt": system_prompt
            }
        )

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
        print("Error during EBITDA Walk analysis and plotting:", str(e))
        return {"type": "text", "data": "Failed to analyze or generate plot due to an error."}
