import type { Database } from "./database-types";

export interface Game {
  id: string;
  created_at: string;
  field_id: number | null;
  my_team_score: number | null;
  opponent_score: number | null;
  position: string | null;
}

export interface Field {
  id: number;
  created_at: string;
  length: number;
  width: number;
  max_lat: number;
  min_lat: number;
  max_lng: number;
  min_lng: number;
  name: string;
  orientation: Database["public"]["Enums"]["orientation"];
}
