import apiClient from '$lib/api-client.js';
import { supabase } from '$lib/supabase-client.js';

const fetchGameData = async (gameId: string) => {
  const gameData = await supabase.from('Game').select().eq('id', gameId);

  let parsedData = null;
  if (!gameData.error && gameData.data && gameData.data.length > 0) {
    parsedData = gameData.data[0]
  }

  return parsedData;
}

const fetchFieldData = async (fieldId: number) => {
  const fieldData = await supabase.from('Field').select().eq('id', fieldId);

  let parsedData = null;
  if (!fieldData.error && fieldData.data && fieldData.data.length > 0) {
    parsedData = fieldData.data[0]
  }

  return parsedData;
}

export const load = async ({ params }) => {
  const gameData = await fetchGameData(params.gameId);

  let fieldData = null;
  if (gameData && gameData.field_id) {
    fieldData = await fetchFieldData(gameData.field_id)
  }

  return {
    game: gameData,
    field: fieldData,
    positions: apiClient.getPositionData(params.gameId)
  };
};
