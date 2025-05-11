import os
from datetime import datetime
from openai import OpenAI
from config.config import MongoDB_Client
from fastapi.responses import JSONResponse
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


## Scrap & Generate Product Data by Generative AI
class Generative_AI_Model:
    def __init__(self) -> JSONResponse:
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.mongodb_session_history_collection = MongoDB_Client().get_collection()

    def __str__(self):
        return "This is an object of Query Response using Generative AI"

    def __repr__(self):
        return (
            "This is an object of Generate response to user query using Generative AI"
        )

    # Store the generated model response in MongoDB with user query
    def stored_session_history_in_MongoDB(
        self, model_type, user_query, model_response
    ) -> None:
        data = {
            "user_query": user_query,
            "model_response": model_response,
            "model_type": model_type,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.mongodb_session_history_collection.insert_one(data)

    # Generate response using OpenAI's chat completion
    def generate_response_from_OPENAI(self, user_query) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "user", "content": user_query},
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()

    # Generate response using Gemini 1.5
    def generate_response_from_Gemini(self, user_query) -> str:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            generation_config=genai.GenerationConfig(
                temperature=0.5,
            ),
        )
        response = model.generate_content(user_query)
        return response.text

    # Generate response according to selected model type
    # and store the session history in MongoDB
    def generate_response_according_selected_model_type(self, model_type, user_query):
        try:
            if model_type == "OpenAI":
                model_response = self.generate_response_from_OPENAI(user_query)
                self.stored_session_history_in_MongoDB(
                    model_type, user_query, model_response
                )
                return JSONResponse(
                    content={"message": model_response}, status_code=200
                )

            elif model_type == "Gemini":
                model_response = self.generate_response_from_Gemini(user_query)
                self.stored_session_history_in_MongoDB(
                    model_type, user_query, model_response
                )
                return JSONResponse(
                    content={"message": model_response}, status_code=200
                )
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=500)

    # Get the session history from MongoDB
    def get_session_history_from_MongoDB(self):
        try:
            session_history = list(
                self.mongodb_session_history_collection.find(
                    {}, projection={"_id": 0, "user_query": 1}
                )
                .sort("_id", -1)
                .limit(10)
            )
            return JSONResponse(content={"message": session_history}, status_code=200)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=500)
