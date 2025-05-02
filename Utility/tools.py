import pandas as pd
from langchain_core.tools import tool
from Utility.plot_ebitda_walk import run_ebitda_walk_analysis_plot
from Utility.plot_ytd import run_ytd_analysis_plot
from Utility.data_analysis import analyze_data
from Utility.llm import llm
from Utility.csv import CSV_EBITDA_WALK, CSV_YTD

try:
    df_ebitda_walk_impact = pd.read_csv(CSV_EBITDA_WALK)
    print("EBITDA Walk CSV loaded successfully.")
except Exception as e:
    print("Error loading EBITDA Walk CSV:", str(e))
    df_ebitda_walk_impact = pd.DataFrame()  # fallback to empty DataFrame

try:
    df_ytd = pd.read_csv(CSV_YTD)
    print("YTD CSV loaded successfully.")
except Exception as e:
    print("Error loading YTD CSV:", str(e))
    df_ytd = pd.DataFrame()  # fallback to empty DataFrame

def create_tools():
    @tool
    def ebitda_walk_tool(query: str) -> dict:
        """
        Tool for generating an EBITDA Walk chart when question involves quarter-to-quarter change.
        """
        print("*********************************************************")
        print("tool :ebitda_walk_tool")
        try:
            image_path = run_ebitda_walk_analysis_plot(df_ebitda_walk_impact, query, llm)
            return {"type": "image", "data": image_path}
        except Exception as e:
            print("Error in ebitda_walk_tool:", str(e))
            return {"type": "text", "data": "Failed to generate EBITDA Walk chart."}

    @tool
    def ytd_plot_tool(query: str) -> dict:
        """
        Tool for generating YTD plots for specific metrics over quarters.
        """
        print("*********************************************************")
        print("tool :ytd_plot_tool")
        try:
            image_path = run_ytd_analysis_plot(df_ytd, query, llm)
            return {"type": "image", "data": image_path}
        except Exception as e:
            print("Error in ytd_plot_tool:", str(e))
            return {"type": "text", "data": "Failed to generate YTD plot."}

    @tool
    def general_text_analysis(query: str) -> dict:
        """
        Tool for handling general financial insights and KPI extraction as plain text.
        """
        print("*********************************************************")
        print("tool :general_text_analysis_tool")
        try:
            response = analyze_data(query, llm, df_ebitda_walk_impact, df_ytd)
            return {"type": "text", "data": response}
        except Exception as e:
            print("Error in general_text_analysis_tool:", str(e))
            return {"type": "text", "data": "Failed to analyze data or generate response."}

    return [ebitda_walk_tool, ytd_plot_tool, general_text_analysis]
