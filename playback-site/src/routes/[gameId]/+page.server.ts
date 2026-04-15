import apiClient from '$lib/api-client.js';
import { createClient } from '@supabase/supabase-js';
import type { Database } from '$lib/types/database-types';
import mockGames from "$lib/mock-data/games.json";

const fetchGameData = async (supabase: ReturnType<typeof createClient<Database>>, gameId: string) => {
  if (import.meta.env.VITE_USE_MOCK_DATA === 'true') {
    return mockGames[0];
  }

  const gameData = await supabase.from('Game').select().eq('id', gameId);

  let parsedData = null;
  if (!gameData.error && gameData.data && gameData.data.length > 0) {
    parsedData = gameData.data[0]
  }

  return parsedData;
}

const fetchFieldData = async (supabase: ReturnType<typeof createClient<Database>>, fieldId: number) => {
  const fieldData = await supabase.from('Field').select().eq('id', fieldId);

  let parsedData = null;
  if (!fieldData.error && fieldData.data && fieldData.data.length > 0) {
    parsedData = fieldData.data[0]
  }

  return parsedData;
}

export const load = async ({ params }) => {
  const supabase = createClient<Database>(import.meta.env.VITE_SUPABASE_URL, import.meta.env.VITE_SUPABASE_KEY);
  const gameData = await fetchGameData(supabase, params.gameId);

  let fieldData = null;
  if (gameData && gameData.field_id) {
    fieldData = await fetchFieldData(supabase, gameData.field_id)
  }

  return {
    game: gameData,
    field: fieldData,
    positions: apiClient.getPositionData(params.gameId)
  };
};
