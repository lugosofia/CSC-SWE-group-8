from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

import mysql.connector

import os

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/get-db-connection")
# Configure the database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
                host=os.getenv("HOST"),
                port=int(os.getenv("PORT")),
                user="admin",
                password=os.getenv("PASSWORD"),
                database=os.getenv("DATABASE")
        )
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        connection.close()
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"message": "Database connection failed: " + str(e)}

@app.get("/")
async def root():
    return {"message": "Hello World"}
