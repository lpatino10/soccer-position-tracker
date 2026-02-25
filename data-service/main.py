from fastapi import FastAPI
from models import WebhookPayload
from epts_generator import create_game_files

app = FastAPI()

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
