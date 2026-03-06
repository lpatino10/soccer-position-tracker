import type { GameData } from "./api-types";

const API_BASE = 'https://soccer-position-tracker.onrender.com';

const getGameData = async (gameId: string): Promise<GameData> => {
  const response = await fetch(`${API_BASE}/game/${gameId}`);
  const { data } = await response.json();
  return data;
}

export default {
  getGameData
}
