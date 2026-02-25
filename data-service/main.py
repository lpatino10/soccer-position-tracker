from datetime import datetime
from fastapi import FastAPI
from models import Game, Field, TrackingEvent
from epts_generator import clean_up_temp_files, generate_metadata, generate_tracking_event_data, MetadataParams, TrackingEventFileParams
from supabase_client import supabase

app = FastAPI()

@app.get("/")
def read_root():
  return { "Hello": "World" }

@app.post("/game/{game_id}")
def create_game_files(game_id: str):
  # 1. Fetch game row in DB to get info like position, score, and field.
  raw_game = supabase.table("Game").select("*").eq("id", game_id).limit(1).execute().data[0]
  game = Game(**raw_game)

  # 2. Fetch field row in DB to get dimensions.
  raw_field = supabase.table("Field").select("*").eq("id", game.field_id).limit(1).execute().data[0]
  field = Field(**raw_field)

  # 3. Fetch TrackingEvent rows to get positions.
  tracking_events = [TrackingEvent(**e) for e in supabase.table("TrackingEvent").select("*").eq("game_id", game.id).order("timestamp", desc=False).execute().data]

  # 4. Create metadata file with parametrized pieces.
  frame_count = len(tracking_events)
  start_datetime = datetime.fromisoformat(tracking_events[0].timestamp)
  end_datetime = datetime.fromisoformat(tracking_events[frame_count - 1].timestamp)
  field_length = 100 if field.length is None else field.length
  field_width = 60 if field.width is None else field.width
  generate_metadata(
    MetadataParams(
      start_datetime=start_datetime,
      end_datetime=end_datetime,
      my_team_score=game.my_team_score,
      opponent_score=game.opponent_score,
      field_length=field_length,
      field_width=field_width,
      field_name=field.name,
      frame_count=frame_count
    )
  )

  # 5. Create event file with locations.
  generate_tracking_event_data(
    TrackingEventFileParams(
      start_datetime=start_datetime,
      field=field,
      tracking_events=tracking_events
    )
  )

  # 6. Cleanup.
  clean_up_temp_files()
