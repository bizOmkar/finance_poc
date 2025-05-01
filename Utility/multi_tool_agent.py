
from Utility.tools import create_tools
from Utility.llm import llm
from prompts.Prompt_multi_tool_agent import prompt
from langchain.agents import AgentType
from langgraph.prebuilt import create_react_agent

def create_multi_tool_agent():
    tools = create_tools()

    agent = create_react_agent(
        llm,
        tools,
        prompt= prompt
    )
    print("*********************************************************")
    print("Reacting Agent call Successfully")
    return agent