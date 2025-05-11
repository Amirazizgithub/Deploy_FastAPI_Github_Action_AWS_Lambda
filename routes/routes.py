from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from model.model import Generative_AI_Model
import warnings

warnings.filterwarnings("ignore")

# Global router
routes = APIRouter()


# Endpoint to respond to user queries via AJAX/Fetch
@routes.post("/query_response")
async def response_of_user_query(request: Request):
    try:
        data = await request.json()
        user_query = data.get("user_query")
        model_type = data.get("model_type")

        if not user_query or not model_type:
            return JSONResponse(
                content={"message": "user_query or model_type is missing"},
                status_code=400,
            )

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
        return JSONResponse(content={"message": str(e)}, status_code=500)
