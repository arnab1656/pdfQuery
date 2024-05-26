# this file is not in use or the components of the Files

import os

from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Define the allowed origins
origins = [
    "http://localhost:3000",  # Frontend application
    # Add other origins if needed
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the directory exists
upload_directory = "uploaded_files"
if not os.path.exists(upload_directory):
    os.makedirs(upload_directory)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")

    file_location = os.path.join(upload_directory, file.filename)
    with open(file_location, "wb") as file_object:
        file_object.write(await file.read())

    return {"info": f"file '{file.filename}' saved at '{file_location}'"}


@app.get("/ask/")
async def ask_question(query: str):

    answer = "The answer is now"
    return JSONResponse(content={"question": query, "answer": answer})
