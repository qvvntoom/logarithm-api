from fastapi import FastAPI
from pydantic import BaseModel
from log_functions import brute_force_method, baby_step_giant_step, pohlig_hellman_algorithm

import io
import sys
import time

app = FastAPI()

class LogInput(BaseModel):
    method: str  # 'brute', 'bsgs', 'pohlig'
    a: int
    b: int
    n: int
    details: bool = True  # domyślnie włączone szczegóły

@app.post("/log")
def compute_log(data: LogInput):
    # Przechwytywanie printów
    buffer = io.StringIO()
    sys_stdout_original = sys.stdout
    sys.stdout = buffer

    try:
        start_time = time.time()

        if data.method == "brute":
            x = brute_force_method(data.a, data.b, data.n, details=data.details)
        elif data.method == "bsgs":
            x = baby_step_giant_step(data.a, data.b, data.n, details=data.details)
        elif data.method == "pohlig":
            x = pohlig_hellman_algorithm(data.a, data.b, data.n, details=data.details)
        else:
            sys.stdout = sys_stdout_original
            return {"error": "Nieznana metoda"}

        elapsed = round(time.time() - start_time, 5)
    except Exception as e:
        sys.stdout = sys_stdout_original
        return {"error": str(e)}

    sys.stdout = sys_stdout_original
    logs = buffer.getvalue()

    return {
        "x": x,
        "time": elapsed,
        "log": logs
    }


