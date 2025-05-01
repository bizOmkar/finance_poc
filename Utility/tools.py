import pandas as pd
from langchain_core.tools import tool
from Utility.plot_ebitda_walk import run_ebitda_walk_analysis_plot
from Utility.plot_ytd import run_ytd_analysis_plot
from Utility.data_analysis import analyze_data

from Utility.llm import llm
# from Utility.csv import df_ebitda_walk_impact, df_ytd
from Utility.csv import CSV_EBITDA_WALK, CSV_YTD


df_ebitda_walk_impact = pd.read_csv(CSV_EBITDA_WALK)
df_ytd = pd.read_csv(CSV_YTD)

def create_tools():
    @tool
    def ebitda_walk_tool(query: str) -> dict:
        """
        Use this tool to generate a detailed EBITDA Walk chart **ONLY** when the question is 
        about how EBITDA changes **from one quarter to another**, like "Q1 to Q3", "Q2 to Q1", etc.
        .
        - Analysis Expectations:
        - Only use the exact row like `EW_QxFY24_QyFY24` to analyze the walk **from Qx to Qy**.
        - Give summary of total EBITDA_Impact and major contributors.
        """
        # return run_ebitda_walk_analysis_plot(final_df, query, llm)
        print("*********************************************************")
        print ("tool :ebitda_walk_tool")
        image_path = run_ebitda_walk_analysis_plot(df_ebitda_walk_impact, query, llm)
        return {"type": "image", "data": image_path}

    @tool
    def ytd_plot_tool(query: str) -> dict:
        """ 
        Use this tool to generate Year-To-Date (YTD) visualizations or when the user asks for a 
        **YTD trend or YTD bar chart** for a quarter.
        - for plots related to 
            Production
            Sales
            Value Added Products
            LME Aluminium
            Strategic Hedging
            Premium
            Realization
            Total Cost
            Alumina
            Power
            Other Hot Metal
            Conversion & Other
            EBITDA Margin
            EBITDA

        Examples:
        - "Plot YTD sales across Q1 to Q3"
        - "Show YTD trend of EBITDA"
        - " Draw bar plot for sales"
        """
        print("*********************************************************")
        print ("tool :ytd_plot_tool")
        image_path = run_ytd_analysis_plot(df_ytd, query, llm)
        return {"type": "image", "data": image_path}
    @tool
    def general_text_analysis(query: str) -> dict:
        """
        Use this tool for general text-based financial insights, including:
        - Quarter-level values (like "Give sales in Q2") for 
        - Stricly Quarter-level KPIs (e.g., "Sales in Q2") use ytd_df as just want give quarter values
        - Retrieval of Data/Number Search (Display results of specific queries ex. Alumina Cost in Q3) use ytd_df
        - Component-wise EBITDA breakdowns
        - Simple summaries or comparisons
        - YTD values in text (not chart form)
        This tool is best when no plot is requested, and the question can be answered in plain text.
        """
        print("*********************************************************")
        print ("tool :general_text_analysis_tool")
        return {"type": "text", "data": analyze_data(query, llm, df_ebitda_walk_impact, df_ytd)}
    
    return [ebitda_walk_tool, ytd_plot_tool, general_text_analysis]