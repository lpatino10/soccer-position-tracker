import apiClient from '$lib/api-client.js';

export const load = async ({ params }) => {
  return { data: apiClient.getGameData(params.gameId) };
};
