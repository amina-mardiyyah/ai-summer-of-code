import os
from model import chat_bot
from fastapi import FastAPI, Request, HttpException
from fastapi.responses import StreamingResponse, PlainTextResponse
from groq import Groq
from dotenv import load_dotenv
load_dotenv()


#initialise application
app = FastAPI()

#initialise chat_bot
chat_bot = chat_bot()

#load api key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

@app.route("/chat_batch", methods=["POST"])

async def chat_batch(request: Request):
    user_input = await request.json()
    user_message = user_input.get('message')
    temperature = float(user_input.get('temperature'))
    selected_model = user_input.get('model')

    #generate response
    try: 
        response = chat_bot.get_response_batch(message=user_message, 
                                            temperature=temperature,
                                            model=selected_model)
        
        output = response.choices[0].message.content

        return PlainTextResponse(content=output, status_code=200)
    
    except Exception as er:
        return {"Error": str(er)}