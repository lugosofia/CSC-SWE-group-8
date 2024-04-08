from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

import mysql.connector

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import os

load_dotenv("/Users/administrator/Desktop/CSC-SWE-group-8/backend/.env")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

print(f"HOST: {os.getenv('HOST')}")
print(f"PORT: {os.getenv('PORT')}")
print(f"USER: {os.getenv('USER')}")
print(f"PASSWORD: {os.getenv('PASSWORD')}")
print(f"DATABASE: {os.getenv('DATABASE')}")

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            port=int(os.getenv("PORT")),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )
        return connection
    except Exception as e:
        raise Exception(f"Failed to connect to the database: {str(e)}")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/questions", response_class=HTMLResponse)
def get_questions(request: Request):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT quest_id, poll_id, quest_txt FROM questions")
        questions = cursor.fetchall()
        connection.close()
        return templates.TemplateResponse("questions.html", {"request": request, "questions": questions})
    except Exception as e:
        return {"message": "Failed to fetch questions: " + str(e)}

@app.post("/submit-answer")
def submit_answer(request: Request, quest_id: int = Form(...), answer_text: str = Form(...)):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO answers (quest_id, answer_text) VALUES (%s, %s)", (quest_id, answer_text))
        connection.commit()
        connection.close()
        return {"message": "Answer submitted successfully"}
    except Exception as e:
        return {"message": "Failed to submit answer: " + str(e)}
