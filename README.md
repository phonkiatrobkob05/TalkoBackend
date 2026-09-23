# Talko Backend

Backend ของโปรเจกต์ Talko (conversational language-learning) — FastAPI + Gemini

## Requirements
- Python 3.14 (pin ให้ทั้งทีมใช้เวอร์ชันเดียวกัน)

## Setup
```powershell
py -3.14 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Config
คัดลอก `.env.example` เป็น `.env` แล้วใส่ `GEMINI_API_KEY` (ขอฟรีจาก Google AI Studio)
```powershell
Copy-Item .env.example .env
```

## Run
```powershell
uvicorn app.main:app --reload
```
เปิด http://127.0.0.1:8000/docs เพื่อลองยิง API ผ่าน Swagger UI

## Endpoints (ปัจจุบัน)
- `GET  /health` — เช็กว่า server ทำงาน
- `POST /chat`   — คุยกับ AI (body: `{ "message": "...", "history": [] }`)
