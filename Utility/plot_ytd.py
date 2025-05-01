import os
from pandasai import Agent
from fastapi.staticfiles import StaticFiles
import matplotlib.pyplot as plt
from io import BytesIO
import base64



def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

def run_ytd_analysis_plot(df_ytd, query, llm):
    print("*********************************************************")
    print(" query, df_ytd received for plotting")
    print("*********************************************************")
    
    agent = Agent(df_ytd, config={
        "llm": llm,
        "cache": None,
        "verbose": True})


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