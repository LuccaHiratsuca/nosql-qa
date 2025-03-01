from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse
from app.use_cases.upload_file import upload_file
from app.use_cases.ask_question import ask_question


app = APIRouter()

@app.post("/upload")
async def upload(file: UploadFile = File(...), user_id: str = Form(...)):
    result = await upload_file(file, user_id)
    return JSONResponse(content=result)

@app.post("/ask")
async def ask(user_id: str = Form(...), question: str = Form(...)):
    result = await ask_question(user_id, question)
    return JSONResponse(content=result)