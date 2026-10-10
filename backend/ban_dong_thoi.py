import sys
from concurrent.futures import ThreadPoolExecutor

import httpx


URL = "http://localhost:8000/api/dang-ky"
PHIEN = sys.argv[1]


def gui(i):
    response = httpx.post(
        URL,
        json={"ma_sv": f"TN{i:03}", "ma_phien": PHIEN},
        timeout=10,
    )
    return response.status_code


with ThreadPoolExecutor(max_workers=40) as executor:
    ma = list(executor.map(gui, range(40)))

print("201:", ma.count(201), "· 409:", ma.count(409))
