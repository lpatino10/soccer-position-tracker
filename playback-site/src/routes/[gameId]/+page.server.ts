import { supabase } from "$lib/supabase-client";

export const load = async ({ params }) => {
  const { data } = await supabase
    .from('TrackingEvent')
    .select()
    .eq('game_id', params.gameId);

  return { data };
};
