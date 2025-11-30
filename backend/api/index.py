from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Research Paper Analyzer API"}

@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    # Lightweight analysis only
    contents = await file.read()
    
    return {
        "filename": file.filename,
        "size": len(contents),
        "status": "success",
        "note": "Full ML analysis requires more resources - deploy to Render/Railway"
    }
