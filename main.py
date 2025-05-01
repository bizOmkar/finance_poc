
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import matplotlib.pyplot as plt
from Utility.dynamic_ebitda_walk import generate_ebitda_walk_from_quarters, fig_to_base64
from Utility.tools import df_ebitda_walk_impact
from Utility.multi_tool_agent import create_multi_tool_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


class QueryRequest(BaseModel):
    query: str
    
class QuarterSelectionRequest(BaseModel):
    source_quarter: str
    target_quarter: str


# Initialize global agent
agent_executor = create_multi_tool_agent()


@app.post("/query")
def query_agent(request: QueryRequest):
    try:
        print("*********************************************************")
        print(f"Query received: {request.query}")
        response = agent_executor.invoke({"messages": [{"content": request.query, "type": "human"}]})
        message_content = response['messages'][-1].content
        print("*********************************************************")
        print(f"message_content: {message_content}")

        # Wrap it in expected format
        return {"response": {"type": "text", "data": message_content}}
    except Exception as e:
        return {"response": {"type": "error", "data": str(e)}}


@app.post("/ebitda-walk-selection")
def ebitda_walk_selection(request: QuarterSelectionRequest):
    source = request.source_quarter
    target = request.target_quarter

    fig = generate_ebitda_walk_from_quarters(df_ebitda_walk_impact, source, target)

    if fig is None:
        return JSONResponse(content={"response": {"type": "text", "data": f"❌ No data found for {source} to {target}."}})

    base64_img = fig_to_base64(fig)
    plt.close(fig)

    return JSONResponse(content={"response": {"type": "image", "data": f"data:image/png;base64,{base64_img}"}})