import { supabase } from "$lib/supabase-client";

export const load = async () => {
  const { data } = await supabase
    .from('Game')
    .select();

  return { data };
};
