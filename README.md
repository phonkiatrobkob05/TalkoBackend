# Talko Backend

Talko Backend

## Requirements
- Python 3.14

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
### Health เช็คว่า Server ทำงานปกติมั้ย
- `GET  /health` — เช็กว่า server ทำงาน
### Chat ใช้ทดสอบในการยิง API สำหรับการคุยมีสองโหมด
- `POST /chat`   — คุยกับ AI (body: `{ "mode": "free|scenario","scenario_id": "0-9", "message": "...", "history": [] }`) 
"mode" - มีแบบ free กับ scenario ถ้าเลือก free เลือก "scenario" เป็น 0 ถ้าเลือก scenario เลือกได้ตั้งแต่ 1-9 
### Scenarios เอาไว้ดูข้อมูลของ Scenario
- `GET /scenarios`  — สำหรับดู scenario ทั้งหมด
### Word เอาไว้ดูคำแปลของคำศัพท์นั้นๆพร้อมตัวอย่าง 
- `GET /word/{word}`  — สำหรับดูคำอ่านคำแปล ตัวอย่างประโยค


