import os
import sqlite3
import threading

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


DB_PATH = os.getenv("DB_PATH", "ngayhoi.db")
SUC_CHUA = 31
db = sqlite3.connect(DB_PATH, check_same_thread=False)
db.execute("""
    CREATE TABLE IF NOT EXISTS dang_ky (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ma_sv TEXT NOT NULL,
        ma_phien TEXT NOT NULL,
        UNIQUE (ma_sv, ma_phien)
    )
""")
db.commit()
db_lock = threading.Lock()

app = FastAPI(title="Đăng ký Ngày hội việc làm")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


class DangKy(BaseModel):
    ma_sv: str
    ma_phien: str


@app.post("/api/dang-ky", status_code=201)
def dang_ky(data: DangKy):
    with db_lock:
        da_dang_ky = db.execute(
            "SELECT 1 FROM dang_ky WHERE ma_sv = ? AND ma_phien = ?",
            (data.ma_sv, data.ma_phien),
        ).fetchone()
        if da_dang_ky:
            raise HTTPException(status_code=409, detail="DA_DANG_KY")

        ket_qua = db.execute(
            """
            INSERT INTO dang_ky (ma_sv, ma_phien)
            SELECT ?, ?
            WHERE (SELECT COUNT(*) FROM dang_ky WHERE ma_phien = ?) < ?
            """,
            (data.ma_sv, data.ma_phien, data.ma_phien, SUC_CHUA),
        )
        db.commit()
        if ket_qua.rowcount == 0:
            raise HTTPException(status_code=409, detail="HET_CHO")
    return {"ok": True}
