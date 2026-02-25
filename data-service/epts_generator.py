from datetime import datetime
from models import Field, Game, TrackingEvent
from pathlib import Path
from pydantic import BaseModel
from supabase_client import supabase
import xml.etree.ElementTree as ET
from xml.dom import minidom

class MetadataParams(BaseModel):
  start_datetime: datetime
  end_datetime: datetime
  my_team_score: int
  opponent_score: int
  field_length: int
  field_width: int
  field_name: str
  frame_count: int

class TrackingEventFileParams(BaseModel):
  start_datetime: datetime
  field: Field
  tracking_events: list[TrackingEvent]

def generate_metadata(params: MetadataParams):
  main = ET.Element("main")
  metadata = ET.SubElement(main, "Metadata")
  global_config = ET.SubElement(metadata, "GlobalConfig")

  file_date = ET.SubElement(global_config, "FileDate")
  file_date.text = datetime.now().isoformat()

  sessions = ET.SubElement(metadata, "Sessions")
  session = ET.SubElement(sessions, "Session", { "id": "session_1" })

  session_start = ET.SubElement(session, "Start")
  session_start.text = params.start_datetime.isoformat()

  session_end = ET.SubElement(session, "End")
  session_end.text = params.end_datetime.isoformat()

  match_params = ET.SubElement(session, "MatchParameters")
  score = ET.SubElement(match_params, "Score", {
    "idLocalTeam": "my_team",
    "idVisitingTeam": "opponent"
  })
  local_team_score = ET.SubElement(score, "LocalTeamScore")
  local_team_score.text = f"{params.my_team_score}"
  visiting_team_score = ET.SubElement(score, "VisitingTeamScore")
  visiting_team_score.text = f"{params.opponent_score}"

  field_size = ET.SubElement(session, "FieldSize")
  length = ET.SubElement(field_size, "Length")
  length.text = f"{params.field_length}"
  width = ET.SubElement(field_size, "Width")
  width.text = f"{params.field_width}"

  teams = ET.SubElement(metadata, "Teams")
  team = ET.SubElement(teams, "Team", { "id": "my_team" })
  team_name = ET.SubElement(team, "Name")
  team_name.text = "My Team"

  players = ET.SubElement(metadata, "Players")
  player = ET.SubElement(players, "Player", {
    "id": "me",
    "teamId": "my_team"
  })
  player_name = ET.SubElement(player, "Name")
  player_name.text = "Logan"

  devices = ET.SubElement(metadata, "Devices")
  device = ET.SubElement(devices, "Device", { "id": "device_1" })
  device_name = ET.SubElement(device, "Name")
  device_name.text = "iPhone GPS"
  sensors = ET.SubElement(device, "Sensors")
  sensor = ET.SubElement(sensors, "Sensor", { "id": "position" })
  sensor_name = ET.SubElement(sensor, "Name")
  sensor_name.text = "Position"
  channels = ET.SubElement(sensor, "Channels")
  channel_x = ET.SubElement(channels, "Channel", { "id": "channel_x" })
  channel_x_name = ET.SubElement(channel_x, "Name")
  channel_x_name.text = "position_x"
  channel_x_unit = ET.SubElement(channel_x, "Unit")
  # TODO: Update unit?
  channel_x_unit.text = "normalized"
  channel_y = ET.SubElement(channels, "Channel", { "id": "channel_y" })
  channel_y_name = ET.SubElement(channel_y, "Name")
  channel_y_name.text = "position_y"
  channel_y_unit = ET.SubElement(channel_y, "Unit")
  # TODO: Update unit?
  channel_y_unit.text = "normalized"

  player_channels = ET.SubElement(metadata, "PlayerChannels")
  ET.SubElement(player_channels, "PlayerChannel", {
    "channelId": "channel_x",
    "id": "me_x",
    "playerId": "me"
  })
  ET.SubElement(player_channels, "PlayerChannel", {
    "channelId": "channel_y",
    "id": "me_y",
    "playerId": "me"
  })

  data_format_specifications = ET.SubElement(main, "DataFormatSpecifications")
  data_format_specification = ET.SubElement(data_format_specifications, "DataFormatSpecification", {
    "separator": ":",
    "startFrame": "1",
    "endFrame": f"{params.frame_count}"
  })
  ET.SubElement(data_format_specification, "StringRegister", {
    "name": "frameCount"
  })
  position_split = ET.SubElement(data_format_specification, "SplitRegister", {
    "separator": ","
  })
  ET.SubElement(position_split, "PlayerChannelRef", {
    "playerChannelId": "me_x"
  })
  ET.SubElement(position_split, "PlayerChannelRef", {
    "playerChannelId": "me_y"
  })

  # Output
  raw_string = ET.tostring(main, "utf-8")
  reparsed = minidom.parseString(raw_string)
  pretty_output = reparsed.toprettyxml(indent="  ")

  temp_file_path = "temp/metadata.xml"
  with open(temp_file_path, "w") as f:
    f.write(pretty_output)

  supabase_file_path = f"{params.field_name}_{params.start_datetime.month}_{params.start_datetime.day}_{params.start_datetime.year}/metadata.xml"
  with open(temp_file_path, "rb") as f:
    supabase.storage.from_("games").upload(
      file=f,
      path=supabase_file_path
    )

def get_normalized_coordinates(field: Field, lng_diff, lat_diff, tracking_event: TrackingEvent):
  norm_x = (tracking_event.lng - field.min_lng) / lng_diff
  norm_y = (tracking_event.lat - field.min_lat) / lat_diff
  return (norm_x, norm_y)

def generate_tracking_event_data(params: TrackingEventFileParams):
  lng_diff = params.field.max_lng - params.field.min_lng
  lat_diff = params.field.max_lat - params.field.min_lat
  
  temp_file_path = "temp/tracking.txt"
  with open(temp_file_path, "w") as f:
    for index, event in enumerate(params.tracking_events):
      coords = get_normalized_coordinates(params.field, lng_diff, lat_diff, event)
      f.write(f"{index + 1}:{coords[0]},{coords[1]}" + "\n")

  supabase_file_path = f"{params.field.name}_{params.start_datetime.month}_{params.start_datetime.day}_{params.start_datetime.year}/tracking.txt"
  with open(temp_file_path, "rb") as f:
    supabase.storage.from_("games").upload(
      file=f,
      path=supabase_file_path
    )

def clean_up_temp_files():
  temp_folder_path = Path("./temp")

  for file in temp_folder_path.iterdir():
    if file.is_file():
        try:
            file.unlink()
        except OSError as e:
            print(f"Error deleting {file}: {e}")

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
