import os
from pandasai import Agent
from fastapi.staticfiles import StaticFiles
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from prompts.Prompt_plot_ebitda_walk import system_prompt

import matplotlib
matplotlib.use('Agg')

def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

def run_ebitda_walk_analysis_plot(df_ebitda_walk_impact, query, llm):
    
    print("*********************************************************")
    print("system_prompt, query, df_ebitda_walk_impact received for plotting")
    print("*********************************************************")
    agent = Agent(
        df_ebitda_walk_impact,
        config={
            "llm": llm,
            "cache": None,
            "verbose": True,
            "system_prompt": system_prompt  # pass system prompt here
        }
    )

    result = agent.chat(query)
    if result:
        print("*********************************************************") 
        print(f"result: {result}")
    else:
        print("No result received from the plot agent.")

    # If `result` is a matplotlib figure
    if isinstance(result, plt.Figure):
        print("Plot Generated Sucessfully")
        return {"type": "image", "data": fig_to_base64(result)}
    else:
        return {"type": "text", "data": result}