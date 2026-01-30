from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import random, os, socket

app = FastAPI()

MENUS = [ "김치찌개", "된장찌개", "제육볶음", "돈까스", "국밥", "비빔밥",
    "라멘", "우동", "초밥", "파스타", "치킨", "피자", "샐러드",
    "쌀국수", "짬뽕", "짜장면", "햄버거", "카레", "순두부찌개" ]

@app.get("/", response_class=HTMLResponse)
def home():
	host = os.getenv("HOSTNAME") or socket.gethostname()
	return f"""
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>점심 룰렛</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Arial; max-width: 520px; margin: 40px auto; padding: 0 16px; }}
    .card {{ border: 1px solid #ddd; border-radius: 12px; padding: 18px; }}
    button {{ padding: 12px 14px; border-radius: 10px; border: 1px solid #ccc; cursor: pointer; margin-right: 8px; }}
    button.primary {{ border-color: #333; }}
    button.danger {{ border-color: #c00; }}
    #result {{ font-size: 28px; margin: 18px 0 6px; }}
    .muted {{ color: #666; font-size: 13px; }}
  </style>
</head>
<body>
  <h1>🍽️ 점심 메뉴 룰렛</h1>
  <div class="card">
    <div id="result">버튼을 눌러주세요</div>
    <div class="muted">host/pod: {host}</div>
    <div style="margin-top:16px;">
      <button class="primary" onclick="spin()">룰렛 돌리기</button>
      <button class="danger" onclick="kill()">자폭(테스트)</button>
    </div>
  </div>

  <script>
    async function spin() {{
      const res = await fetch('/api/spin');
      const data = await res.json();
      document.getElementById('result').innerText = data.menu;
    }}

    async function kill() {{
      // 이 요청 이후 서버 프로세스가 종료됩니다.
      await fetch('/api/kill', {{ method: 'POST' }});
    }}
  </script>
</body>
</html>
"""

@app.get("/api/spin")
def spin():
    menu = random.choice(MENUS)
    return JSONResponse({"menu": menu})

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/api/kill")
def kill():
    # 데모용: 프로세스 즉시 종료 (Docker/k8s에서 self-healing 확인용)
    os._exit(1)

