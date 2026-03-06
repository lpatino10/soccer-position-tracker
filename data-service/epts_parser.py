from kloppy import metrica
# from kloppy.domain import CustomCoordinateSystem, Dimension, Origin, PitchDimensions, Unit

bucket_base_url = "https://paugmeoshsaakpmuwsoo.supabase.co/storage/v1/object/public/games"

# my_coordinate_system = CustomCoordinateSystem(
#   origin=Origin.BOTTOM_LEFT,
  # pitch_dimensions=NormalizedPitchDimensions(
  #   pitch_length=105,
  #   pitch_width=68,
  # ),
# )

# my_pitch_dimensions = PitchDimensions(
#   unit=Unit.NORMED,
#   standardized=True,
#   x_dim=Dimension(min=0, max=1),
#   y_dim=Dimension(min=0, max=1),
  # pitch_length=,
  # pitch_width=
# )

def parse_game_data(game_id: str) -> list[dict[str, int]]:
  dataset = metrica.load_tracking_epts(
    meta_data=f"{bucket_base_url}/{game_id}/metadata.xml?cache=v1",
    raw_data=f"{bucket_base_url}/{game_id}/tracking.txt?cache=v1",
    coordinates="metrica",
  )

  full_df = dataset.to_df()
  player_position_subset = full_df[["me_x", "me_y"]].rename(columns={"me_x": "x", "me_y": "y"})
  return player_position_subset.to_dict(orient="records")
