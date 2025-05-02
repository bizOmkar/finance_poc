from Utility.tools import create_tools
from Utility.llm import llm
from prompts.Prompt_multi_tool_agent import prompt

from langgraph.prebuilt import create_react_agent

def create_multi_tool_agent():
    try:
        tools = create_tools()
        if llm is None:
            raise ValueError("LLM is not initialized properly.")

        agent = create_react_agent(
            llm,
            tools,
            prompt=prompt
        )
        print("*********************************************************")
        print("Reacting Agent call Successfully")
        return agent

    except Exception as e:
        print("Error while creating multi-tool agent:", str(e))
        return None
