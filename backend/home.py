from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

import mysql.connector

import os

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/questions", response_class=HTMLResponse)
def get_questions(request: Request):
    try:
        connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            port=int(os.getenv("PORT")),
            user="admin",
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )
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
        connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            port=int(os.getenv("PORT")),
            user="admin",
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO answers (quest_id, answer_text) VALUES (%s, %s)", (quest_id, answer_text))
        connection.commit()
        connection.close()
        return {"message": "Answer submitted successfully"}
    except Exception as e:
        return {"message": "Failed to submit answer: " + str(e)}