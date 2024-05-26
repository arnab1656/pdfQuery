import os

from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from helper.answerGenerator import generate_text_from_pdf

app = FastAPI()

# Define the allowed origins


origins = [
    "http://localhost:3000",  # Frontend application
]

# Allow middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Ensure the directory exists
upload_directory = "uploaded_files"
if not os.path.exists(upload_directory):
    os.makedirs(upload_directory)


@app.get("/")
def read_root():
    return {"health": "Welcome to the FastAPI applicationa and the server is On"}


# Define a GET route
@app.get("/hello")
async def hello():
    return {"message": "Hello, world!"}


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...), query: Optional[str] = None):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")

    # Check if the file already exists in the directory
    # else the file is created in the directory

    file_location = os.path.join(upload_directory, file.filename)
    if os.path.isfile(file_location):
        return {"info": f"file '{file.filename}' is already in '{file_location}'"}
    else:
        file_location = os.path.join(upload_directory, file.filename)
        with open(file_location, "wb") as file_object:
            file_object.write(await file.read())

        return {"info": f"file '{file.filename}' saved at '{file_location}'"}


@app.get("/ask/")
async def ask_question(query: str, query2: str):
    answer = "The answer is now"

    answer = generate_text_from_pdf(query, query2)
    
    return JSONResponse(content={"question": query, "answer": answer})
