import type { PositionData } from "./api-types";

const API_BASE = 'https://soccer-position-tracker.onrender.com';

const getPositionData = async (gameId: string): Promise<PositionData> => {
  const response = await fetch(`${API_BASE}/game/${gameId}`);
  const { data } = await response.json();
  return data;
}

export default {
  getPositionData
}
