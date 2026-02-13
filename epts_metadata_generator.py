from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

main = ET.Element("main")

metadata = ET.SubElement(main, "Metadata")

global_config = ET.SubElement(metadata, "GlobalConfig")

# TODO: Parametrize.
file_date = ET.SubElement(global_config, "FileDate")
file_date.text = datetime.now().isoformat()

sessions = ET.SubElement(metadata, "Sessions")
session = ET.SubElement(sessions, "Session", { "id": "session_1" })

# TODO: Parametrize.
session_start = ET.SubElement(session, "Start")
session_start.text = datetime.now().isoformat()

# TODO: Parametrize.
session_end = ET.SubElement(session, "End")
session_end.text = datetime.now().isoformat()

# TODO: Parametrize.
match_params = ET.SubElement(session, "MatchParameters")
score = ET.SubElement(match_params, "Score", {
  "idLocalTeam": "my_team",
  "idVisitingTeam": "visitor"
})
local_team_score = ET.SubElement(score, "LocalTeamScore")
local_team_score.text = "0"
visiting_team_score = ET.SubElement(score, "VisitingTeamScore")
visiting_team_score.text = "0"

# TODO: Parametrize.
field_size = ET.SubElement(session, "FieldSize")
length = ET.SubElement(field_size, "Length")
length.text = "68"
width = ET.SubElement(field_size, "Width")
width.text = "105"

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

# TODO: Parametrize.
data_format_specifications = ET.SubElement(main, "DataFormatSpecifications")
data_format_specification = ET.SubElement(data_format_specifications, "DataFormatSpecification", {
  "separator": ":",
  "startFrame": "1",
  # TODO: UPDATE!
  "endFrame": "100"
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
with open("epts_metadata.xml", "w") as f:
  f.write(pretty_output)
