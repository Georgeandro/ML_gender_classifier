from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastai.vision.all import load_learner, PILImage
from io import BytesIO

app = FastAPI()

# Ensure the correct path to your exported model
learn = load_learner('/app/export.pkl')

@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    img = PILImage.create(BytesIO(await file.read()))
    pred, _, probs = learn.predict(img)
    return JSONResponse(content={"prediction": pred})
