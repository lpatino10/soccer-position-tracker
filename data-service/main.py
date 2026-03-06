from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from models import WebhookPayload
from epts_generator import create_game_files
from epts_parser import parse_game_data

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
  print(jsonable_encoder({"detail": exc.errors(), "body": exc.body}))
  return JSONResponse(
    status_code=422,
    content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
  )

@app.get("/")
def read_root():
  return { "Hello": "World" }

@app.post("/game")
def create_game_files_from_webhook(body: WebhookPayload):
  create_game_files(body.record.id)

@app.post("/game/{game_id}")
def create_game_files_from_id(game_id: str):
  """
  Used mostly for manual testing.
  """
  create_game_files(game_id)

@app.get("/game/{game_id}")
def get_game_positions(game_id: str):
  game_data = parse_game_data(game_id)
  return {
    "data": game_data
  }
