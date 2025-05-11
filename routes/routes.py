from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from model.model import Generative_AI_Model
import warnings

warnings.filterwarnings("ignore")

## Global Route
routes = APIRouter()

## Routes for Generative AI Model APIs


# Endpoint to response of the user query
# This endpoint is intended to be called via AJAX/Fetch
@routes.post("/query_response")
async def response_of_user_query(request: Request):
    try:
        data = await request.json()

        user_query = data["user_query"]
        model_type = data["model_type"]

        generative_ai_model = Generative_AI_Model()
        return generative_ai_model.generate_response_according_selected_model_type(
            model_type=model_type, user_query=user_query
        )

    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)


# Endpoint to fetch last 10 session history
@routes.get("/session_history")
async def get_session_history():
    try:
        generative_ai_model = Generative_AI_Model()
        return generative_ai_model.get_session_history_from_MongoDB()
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)


# Endpoint to check health of the service
@routes.get("/health")
async def get_health_check():
    try:
        return JSONResponse(
            content={"message": "Service Health is Good"}, status_code=200
        )
    except Exception as e:
        print(f"Error in /session_history: {e}")
        return JSONResponse(content={"message": str(e)}, status_code=500)
