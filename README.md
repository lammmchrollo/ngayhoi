# Bài thực hành 4 — Phạm Tùng Lâm — 23110320

Cổng đăng ký Ngày hội việc làm, tiếp nối Buổi 3. Buổi 4 thêm giới hạn 30 chỗ cho từng phiên, kiểm thử tự động và thí nghiệm 40 yêu cầu đồng thời.

## Chạy máy chủ

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

## Kiểm tra

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
```
