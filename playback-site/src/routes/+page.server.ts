import { createClient } from '@supabase/supabase-js';
import type { Database } from '$lib/types/database-types';
import mockGames from "$lib/mock-data/games.json";

export const load = async () => {
  if (import.meta.env.VITE_USE_MOCK_DATA === 'true') {
    return { data: mockGames };
  }

  const supabase = createClient<Database>(import.meta.env.VITE_SUPABASE_URL, import.meta.env.VITE_SUPABASE_KEY);
  const { data } = await supabase
    .from('Game')
    .select();

  return { data };
};
