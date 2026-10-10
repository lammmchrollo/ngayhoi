import os

os.environ["DB_PATH"] = ":memory:"

import pytest
from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


@pytest.fixture(autouse=True)
def so_trong():
    with main.db_lock:
        main.db.execute("DELETE FROM dang_ky")
        main.db.commit()


def lap_day(ma_phien, n):
    for i in range(n):
        response = client.post(
            "/api/dang-ky",
            json={"ma_sv": f"SV{i:03}", "ma_phien": ma_phien},
        )
        assert response.status_code == 201


def test_phien_trong_dang_ky_thanh_cong():
    response = client.post("/api/dang-ky", json={"ma_sv": "SV001", "ma_phien": "P01"})
    assert response.status_code == 201
    assert response.json() == {"ok": True}


def test_nguoi_thu_30_duoc_dang_ky():
    lap_day("P01", 29)
    response = client.post("/api/dang-ky", json={"ma_sv": "SV030", "ma_phien": "P01"})
    assert response.status_code == 201


def test_nguoi_thu_31_bi_tu_choi_het_cho():
    lap_day("P01", 30)
    response = client.post("/api/dang-ky", json={"ma_sv": "SV031", "ma_phien": "P01"})
    assert response.status_code == 409
    assert response.json() == {"detail": "HET_CHO"}


def test_dang_ky_lai_duoc_bao_da_dang_ky_khi_phien_day():
    lap_day("P01", 30)
    response = client.post("/api/dang-ky", json={"ma_sv": "SV000", "ma_phien": "P01"})
    assert response.status_code == 409
    assert response.json() == {"detail": "DA_DANG_KY"}


def test_phien_khac_van_con_cho():
    lap_day("P01", 30)
    response = client.post("/api/dang-ky", json={"ma_sv": "SV031", "ma_phien": "P02"})
    assert response.status_code == 201
