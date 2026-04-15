import mockTrackingEvents from "$lib/mock-data/tracking-events.json";
import type { PositionData } from "./types/api-types";

const API_BASE = 'https://soccer-position-tracker.onrender.com';

const getPositionData = async (gameId: string): Promise<PositionData> => {
  if (import.meta.env.VITE_USE_MOCK_DATA === 'true') {
    return mockTrackingEvents;
  }

  const response = await fetch(`${API_BASE}/game/${gameId}`);
  const { data } = await response.json();
  return data;
}

export default {
  getPositionData
}
