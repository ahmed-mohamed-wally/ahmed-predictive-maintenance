from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.inference import predict_machine


app = FastAPI(
    title="Predictive Maintenance API",
    description="API for machine failure and failure-type prediction",
    version="1.0.0",
)

# Allow the local dashboard (opened from file://) to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MachineInput(BaseModel):
    machine_type: str
    air_temp: float
    process_temp: float
    rpm: float
    torque: float
    tool_wear: float


@app.get("/")
def root():
    return {
        "message": "Predictive Maintenance API is running"
    }


@app.post("/predict")
def predict(data: MachineInput):
    try:
        result = predict_machine(
            machine_type=data.machine_type,
            air_temp=data.air_temp,
            process_temp=data.process_temp,
            rpm=data.rpm,
            torque=data.torque,
            tool_wear=data.tool_wear,
        )

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc
