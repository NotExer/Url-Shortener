from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import random
import string
import os

app = FastAPI()

# Mount static files
app.mount("/img", StaticFiles(directory="img"), name="img")

# Base de datos en memoria
urls = {}

def generate_code():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/shorten")
async def LinkShort(original_url: str, request: Request):
    code = generate_code()
    urls[code] = original_url
    base_url = str(request.base_url)
    return {"short_url": f"{base_url}{code}", "code": code}

@app.get("/{code}")
async def redirect_to_url(code: str):
    if code in urls:
        return RedirectResponse(url=urls[code])
    raise HTTPException(status_code=404, detail="URL no encontrada")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)