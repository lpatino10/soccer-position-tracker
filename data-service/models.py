from decimal import Decimal
from pydantic import BaseModel

class Game(BaseModel):
  id: str
  created_at: str
  position: str
  my_team_score: int
  opponent_score: int
  field_id: int

class Field(BaseModel):
  id: int
  created_at: str
  name: str
  length: int
  width: int
  min_lat: Decimal
  max_lat: Decimal
  min_lng: Decimal
  max_lng: Decimal

class TrackingEvent(BaseModel):
  id: str
  created_at: str
  timestamp: str
  lat: Decimal
  lng: Decimal
  game_id: str

class WebhookPayload(BaseModel):
  type: str
  table: str
  schema: str
  record: Game
  old_record: Game
