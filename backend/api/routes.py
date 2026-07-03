from pathlib import Path
import shutil

# from fastapi import APIRouter, UploadFile, File, HTTPError, Response
from fastapi import APIRouter, UploadFile, File, HTTPException

from services.analyzer import analyze_log, get_history, delete_history_item


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


@router.get("/history")
def fetch_history():
    return get_history()


@router.delete("/history/{analysis_id}")
def delete_history(analysis_id: str):
    success = delete_history_item(analysis_id)
    if success:
        return {"status": "success", "message": f"Item {analysis_id} deleted."}
    # return {"status": "error", "message": "Failed to delete item."}
    raise HTTPException(status_code=404, detail="Item not found")