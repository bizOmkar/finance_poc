from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import matplotlib.pyplot as plt
from Utility.dynamic_ebitda_walk import generate_ebitda_walk_from_quarters, fig_to_base64
from Utility.tools import df_ebitda_walk_impact
from Utility.multi_tool_agent import create_multi_tool_agent


# Initialize FastAPI app
app = FastAPI()

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent once
try:
    agent_executor = create_multi_tool_agent()
except Exception as e:
    agent_executor = None
    print("❌ Error initializing agent_executor:", str(e))


# Request body for LLM query
class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_agent(request: QueryRequest):
    try:
        print("*********************************************************")
        print(f"Query received: {request.query}")
        
        if agent_executor is None:
            raise RuntimeError("Agent executor not initialized.")

        response = agent_executor.invoke({
            "messages": [{"content": request.query, "type": "human"}]
        })
        message_content = response['messages'][-1].content

        print("*********************************************************")
        print(f"message_content: {message_content}")

        return {"response": {"type": "text", "data": message_content}}

    except Exception as e:
        return {"response": {"type": "error", "data": str(e)}}


# Request body for EBITDA walk selection
class QuarterSelectionRequest(BaseModel):
    source_quarter: str
    target_quarter: str

@app.post("/ebitda-walk-selection")
def ebitda_walk_selection(request: QuarterSelectionRequest):
    try:
        source = request.source_quarter
        target = request.target_quarter

        fig = generate_ebitda_walk_from_quarters(df_ebitda_walk_impact, source, target)

        if fig is None:
            return JSONResponse(content={
                "response": {"type": "text", "data": f"❌ No data found for {source} to {target}."}
            })

        base64_img = fig_to_base64(fig)
        plt.close(fig)

        return JSONResponse(content={
            "response": {"type": "image", "data": f"data:image/png;base64,{base64_img}"}
        })

    except Exception as e:
        return JSONResponse(content={
            "response": {"type": "error", "data": f"❌ Internal error: {str(e)}"}
        })
