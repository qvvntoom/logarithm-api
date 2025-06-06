from fastapi import FastAPI
from pydantic import BaseModel
from log_functions import brute_force_method, baby_step_giant_step, pohlig_hellman_algorithm

app = FastAPI()

class LogInput(BaseModel):
    method: str  # 'brute', 'bsgs', 'pohlig'
    a: int
    b: int
    n: int

@app.post("/log")
def compute_log(data: LogInput):
    try:
        if data.method == "brute":
            x = brute_force_method(data.a, data.b, data.n)
        elif data.method == "bsgs":
            x = baby_step_giant_step(data.a, data.b, data.n)
        elif data.method == "pohlig":
            x = pohlig_hellman_algorithm(data.a, data.b, data.n)
        else:
            return {"error": "Nieznana metoda"}
        return {"x": x}
    except Exception as e:
        return {"error": str(e)}
