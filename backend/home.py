from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.params import Path
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from typing import Union

import mysql.connector

import os

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            port=int(os.getenv("PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )
        return connection
    except Exception as e:
        raise Exception(f"Failed to connect to the database: {str(e)}")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Render the dashboard template
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/recent_polls", response_class=HTMLResponse)
def get_recent_polls(request: Request):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM polls ORDER BY start_date DESC")
        recent_polls = cursor.fetchall()
        latest_poll = recent_polls[0] if recent_polls else None
        print(latest_poll)
        connection.close()
        return templates.TemplateResponse("recent_polls.html", {"request": request, "recent_polls": recent_polls, "latest_poll": latest_poll})
    except Exception as e:
        return {"message": "Failed to fetch recent polls: " + str(e)}

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

@app.get("/results", response_class=HTMLResponse)
def get_results(request: Request):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT answer_id, answer_text FROM answers")
        results = cursor.fetchall()
        connection.close()
        return templates.TemplateResponse("results.html", {"request": request, "results": results})
    except Exception as e:
        return {"message": "Failed to answers questions: " + str(e)}

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT user_id, username, user_type, password FROM users WHERE username = %s AND password = %s"
    values = (username, password)
    cursor.execute(query, values)
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:
        user_type= user[2] # Assuming 'user_type' is a column in the 'users' table

        print(f"User type: {user_type}") # Debug statement

        if user_type == 'admin':
            return RedirectResponse("/dashboard", status_code=302)
        elif user_type == 'user':
            return RedirectResponse("/recent_polls", status_code=302)
        else:
            raise HTTPException(status_code=403, detail="Invald user type")
    else:
        # Invalid credentials
        raise HTTPException(status_code=401, detail="Invalid username or password")

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

@app.delete("/delete-answer/{answer_id}")
def delete_answer(answer_id: int = Path(..., gt=0)):
    print(f"Received answer_id: {answer_id}")
    try:
        connection = get_db_connection()
        cursor =connection.cursor()
        cursor.execute("DELETE FROM answers WHERE answer_id = %s", (answer_id,))
        connection.commit()
        connection.close()
        return {"message": "Answer deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete answer: " + str(e))

@app.delete("/delete-poll/{poll_id}")
async def delete_poll(poll_id: int = Path(..., gt=0)):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM polls WHERE id = %s", (poll_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Poll deleted successfully"}
