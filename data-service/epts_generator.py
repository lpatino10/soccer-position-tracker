from datetime import datetime
from models import SoccerField, Game, TrackingEvent
from pathlib import Path
from pydantic import BaseModel
from supabase_client import supabase
import xml.etree.ElementTree as ET
from xml.dom import minidom

class MetadataParams(BaseModel):
  game_id: str
  start_datetime: datetime
  end_datetime: datetime
  my_team_score: int
  opponent_score: int
  field_length: int
  field_width: int
  field_name: str
  frame_count: int

class TrackingEventFileParams(BaseModel):
  game_id: str
  field: SoccerField
  tracking_events: list[TrackingEvent]

def generate_metadata(params: MetadataParams):
  main = ET.Element("main")
  metadata = ET.SubElement(main, "Metadata")
  global_config = ET.SubElement(metadata, "GlobalConfig")

  file_date = ET.SubElement(global_config, "FileDate")
  file_date.text = datetime.now().isoformat()
  provider_name = ET.SubElement(global_config, "ProviderName")
  provider_name.text = "lopa inc."
  frame_rate = ET.SubElement(global_config, "FrameRate")
  frame_rate.text = "120"
  provider_params = ET.SubElement(global_config, "ProviderGlobalParameters")
  first_half_start_param = ET.SubElement(provider_params, "ProviderParameter")
  first_half_start_name = ET.SubElement(first_half_start_param, "Name")
  first_half_start_name.text = "first_half_start"
  first_half_start_value = ET.SubElement(first_half_start_param, "Value")
  first_half_start_value.text = "1"
  first_half_end_param = ET.SubElement(provider_params, "ProviderParameter")
  first_half_end_name = ET.SubElement(first_half_end_param, "Name")
  first_half_end_name.text = "first_half_end"
  first_half_end_value = ET.SubElement(first_half_end_param, "Value")
  # TODO: Figure out a way to specify the actual split between halves.
  first_half_end_value.text = f"{params.frame_count - 2}"
  second_half_start_param = ET.SubElement(provider_params, "ProviderParameter")
  second_half_start_name = ET.SubElement(second_half_start_param, "Name")
  second_half_start_name.text = "second_half_start"
  second_half_start_value = ET.SubElement(second_half_start_param, "Value")
  second_half_start_value.text = f"{params.frame_count - 1}"
  second_half_end_param = ET.SubElement(provider_params, "ProviderParameter")
  second_half_end_name = ET.SubElement(second_half_end_param, "Name")
  second_half_end_name.text = "second_half_end"
  second_half_end_value = ET.SubElement(second_half_end_param, "Value")
  second_half_end_value.text = f"{params.frame_count}"


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
  # Weird that this isn't Length, but that's what the Metrica adaptor expects.
  height = ET.SubElement(field_size, "Height")
  height.text = f"{params.field_length}"
  width = ET.SubElement(field_size, "Width")
  width.text = f"{params.field_width}"

  teams = ET.SubElement(metadata, "Teams")
  my_team = ET.SubElement(teams, "Team", { "id": "my_team" })
  team_name = ET.SubElement(my_team, "Name")
  team_name.text = "My Team"
  # TODO: Make attacking direction dynamic.
  my_team_provider_params = ET.SubElement(my_team, "ProviderTeamsParameters")
  my_team_provider_param = ET.SubElement(my_team_provider_params, "ProviderParameter")
  my_team_provider_param_name = ET.SubElement(my_team_provider_param, "Name")
  my_team_provider_param_name.text = "attack_direction_first_half"
  my_team_provider_param_value = ET.SubElement(my_team_provider_param, "Value")
  my_team_provider_param_value.text = "right_to_left"
  opponent = ET.SubElement(teams, "Team", { "id": "opponent" })
  opponent_team_name = ET.SubElement(opponent, "Name")
  opponent_team_name.text = "Opponent"
  opponent_provider_params = ET.SubElement(opponent, "ProviderTeamsParameters")
  opponent_provider_param = ET.SubElement(opponent_provider_params, "ProviderParameter")
  opponent_provider_param_name = ET.SubElement(opponent_provider_param, "Name")
  opponent_provider_param_name.text = "attack_direction_first_half"
  opponent_provider_param_value = ET.SubElement(opponent_provider_param, "Value")
  opponent_provider_param_value.text = "left_to_right"

  players = ET.SubElement(metadata, "Players")
  player = ET.SubElement(players, "Player", {
    "id": "me",
    "teamId": "my_team"
  })
  player_name = ET.SubElement(player, "Name")
  player_name.text = "Logan"
  shirt_number = ET.SubElement(player, "ShirtNumber")
  shirt_number.text = "10"

  devices = ET.SubElement(metadata, "Devices")
  device = ET.SubElement(devices, "Device", { "id": "device_1" })
  device_name = ET.SubElement(device, "Name")
  device_name.text = "iPhone GPS"
  sensors = ET.SubElement(device, "Sensors")
  sensor = ET.SubElement(sensors, "Sensor", { "id": "position" })
  sensor_name = ET.SubElement(sensor, "Name")
  sensor_name.text = "Position"
  channels = ET.SubElement(sensor, "Channels")
  channel_x = ET.SubElement(channels, "Channel", { "id": "x" })
  channel_x_name = ET.SubElement(channel_x, "Name")
  channel_x_name.text = "position_x"
  channel_x_unit = ET.SubElement(channel_x, "Unit")
  # TODO: Update unit?
  channel_x_unit.text = "normalized"
  channel_y = ET.SubElement(channels, "Channel", { "id": "y" })
  channel_y_name = ET.SubElement(channel_y, "Name")
  channel_y_name.text = "position_y"
  channel_y_unit = ET.SubElement(channel_y, "Unit")
  # TODO: Update unit?
  channel_y_unit.text = "normalized"

  player_channels = ET.SubElement(metadata, "PlayerChannels")
  ET.SubElement(player_channels, "PlayerChannel", {
    "channelId": "x",
    "id": "me_x",
    "playerId": "me"
  })
  ET.SubElement(player_channels, "PlayerChannel", {
    "channelId": "y",
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
  player_section_split = ET.SubElement(data_format_specification, "SplitRegister", {
    "separator": ","
  })
  ET.SubElement(player_section_split, "PlayerChannelRef", {
    "playerChannelId": "me_x"
  })
  ET.SubElement(player_section_split, "PlayerChannelRef", {
    "playerChannelId": "me_y"
  })
  ball_section_split = ET.SubElement(data_format_specification, "SplitRegister", {
    "separator": ","
  })
  ET.SubElement(ball_section_split, "BallChannelRef", {
    "channelId": "x"
  })
  ET.SubElement(ball_section_split, "BallChannelRef", {
    "channelId": "y"
  })

  # Output
  raw_string = ET.tostring(main, "utf-8")
  reparsed = minidom.parseString(raw_string)
  pretty_output = reparsed.toprettyxml(indent="  ")

  # Create temp folder if necessary.
  temp_folder = Path("temp")
  temp_folder.mkdir(parents=True, exist_ok=True)

  temp_file_path = "temp/metadata.xml"
  with open(temp_file_path, "w") as f:
    f.write(pretty_output)

  supabase_file_path = f"{params.game_id}/metadata.xml"
  with open(temp_file_path, "rb") as f:
    supabase.storage.from_("games").upload(
      file=f,
      path=supabase_file_path
    )

def get_normalized_coordinates(field: SoccerField, lng_diff, lat_diff, tracking_event: TrackingEvent):
  if field.orientation == "EW":
    norm_x = (tracking_event.lng - field.min_lng) / lng_diff
    norm_y = (tracking_event.lat - field.min_lat) / lat_diff
    return (norm_x, norm_y)
  elif field.orientation == "NS":
    norm_x = (tracking_event.lat - field.min_lat) / lat_diff
    norm_y = 1 - ((tracking_event.lng - field.min_lng) / lng_diff)
    return (norm_x, norm_y)

def generate_tracking_event_data(params: TrackingEventFileParams):
  lng_diff = params.field.max_lng - params.field.min_lng
  lat_diff = params.field.max_lat - params.field.min_lat
  
  temp_file_path = "temp/tracking.txt"
  with open(temp_file_path, "w") as f:
    for index, event in enumerate(params.tracking_events):
      coords = get_normalized_coordinates(params.field, lng_diff, lat_diff, event)
      f.write(f"{index + 1}:{coords[0]},{coords[1]}:0,0" + "\n")

  supabase_file_path = f"{params.game_id}/tracking.txt"
  with open(temp_file_path, "rb") as f:
    supabase.storage.from_("games").upload(
      file=f,
      path=supabase_file_path
    )

def clean_up_temp_files():
  temp_folder_path = Path("temp")

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
  field = SoccerField(**raw_field)

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
      game_id=game_id,
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
      game_id=game_id,
      field=field,
      tracking_events=tracking_events
    )
  )

  # 6. Cleanup.
  clean_up_temp_files()
