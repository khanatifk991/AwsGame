from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import random
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

secret_number = random.randint(1, 100)
attempts = 0

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def process_guess(request: Request, guess: int = Form(...)):
    global secret_number, attempts  # Declare the variables as global
    attempts += 1
    if guess == secret_number:
        message = f"Congratulations! You guessed the number {secret_number} in {attempts} attempts."
        secret_number = random.randint(1, 100)
        attempts = 0
    elif guess < secret_number:
        message = "Try a higher number."
    else:
        message = "Try a lower number."
    return templates.TemplateResponse("index.html", {"request": request, "message": message})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
