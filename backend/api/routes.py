from pathlib import Path
import shutil

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from services.analyzer import analyze_log


router = APIRouter()


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.get("/health")
def health():

    return {
        "status": "healthy"
    }


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_log(file_path)

    return result