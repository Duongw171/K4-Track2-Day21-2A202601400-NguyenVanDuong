from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import joblib
import os

app = FastAPI()

ARTIFACT_BUCKET = os.environ["ARTIFACT_BUCKET"]
MODEL_KEY = "artifacts/current/model.joblib"
MODEL_PATH = os.path.expanduser("~/models/model.joblib")


def download_model():
    """
    Tai file model.joblib tu AWS S3 ve may khi server khoi dong.
    Su dung AWS credentials cau hinh trong moi truong / systemd service.
    """
    s3 = boto3.client("s3")
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    s3.download_file(ARTIFACT_BUCKET, MODEL_KEY, MODEL_PATH)
    print(f"Model da duoc tai xuong tu s3://{ARTIFACT_BUCKET}/{MODEL_KEY}")


download_model()
model = joblib.load(MODEL_PATH)


class ScoreRequest(BaseModel):
    features: list[float]


@app.get("/healthz")
def healthz():
    """Endpoint kiem tra suc khoe server."""
    return {"status": "ok"}


@app.post("/score")
def score(req: ScoreRequest):
    """
    Endpoint suy luan chinh.
    Dau vao : JSON {"features": [f1, f2, ..., f10]}
    Dau ra  : JSON {"prediction": <0|1>, "label": <"thu_nhap_thap"|"thu_nhap_cao">}
    """
    if len(req.features) != 10:
        raise HTTPException(
            status_code=400,
            detail="Expected 10 features (adult income)"
        )

    pred = model.predict([req.features])
    prediction = int(pred[0])
    label = "thu_nhap_cao" if prediction == 1 else "thu_nhap_thap"
    return {"prediction": prediction, "label": label}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
