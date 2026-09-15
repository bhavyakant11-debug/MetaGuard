from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import uuid

from ocr import extract_text
from rules import check_compliance
from database import (
    create_table,
    save_inspection,
    get_inspections,
    get_inspection_by_id,
    generate_report
)

app = FastAPI(
    title="Metraguard API",
    description="AI-powered Legal Metrology Compliance System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

create_table()


@app.get("/")
def home():
    return {
        "message": "Metraguard backend is running!",
        "status": "online"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/analyze")
async def analyze_product(file: UploadFile = File(...)):

    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/jpg",
        "image/webp",
        "image/jfif"
    ]

    if file.content_type not in allowed_types:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Please upload a valid product image."
            }
        )

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    file_path = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    extracted_text = extract_text(file_path)

    compliance_result = check_compliance(extracted_text)

    inspection_id = save_inspection(
        filename=unique_filename,
        compliance_status=compliance_result["compliance_status"],
        compliance_score=compliance_result["compliance_score"],
        extracted_text=extracted_text,
        violations=compliance_result["violations"]
    )

    return {
        "inspection_id": inspection_id,
        "message": "Product image analyzed successfully",
        "filename": unique_filename,
        "status": "analysis_complete",
        "extracted_text": extracted_text,
        "compliance": compliance_result
    }


@app.get("/inspections")
def view_inspections():

    inspections = get_inspections()

    results = []

    for inspection in inspections:
        results.append({
            "id": inspection[0],
            "filename": inspection[1],
            "compliance_status": inspection[2],
            "compliance_score": inspection[3],
            "violations": inspection[4]
        })

    return {
        "total_inspections": len(results),
        "inspections": results
    }


@app.get("/inspection/{inspection_id}")
def view_inspection(inspection_id: int):

    inspection = get_inspection_by_id(inspection_id)

    if inspection is None:
        return {
            "error": "Inspection not found"
        }

    return {
        "id": inspection[0],
        "filename": inspection[1],
        "compliance_status": inspection[2],
        "compliance_score": inspection[3],
        "extracted_text": inspection[4],
        "violations": inspection[5].split("\n")
    }


@app.get("/inspection/{inspection_id}/report")
def inspection_report(inspection_id: int):

    report = generate_report(inspection_id)

    if report is None:
        return {
            "error": "Inspection not found"
        }

    return {
        "inspection_id": inspection_id,
        "report": report
    }