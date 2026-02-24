import { createClient } from '@supabase/supabase-js'
import { type Database } from '$lib/database.types';

export const supabase = createClient<Database>('https://paugmeoshsaakpmuwsoo.supabase.co', 'sb_publishable_YW4rIYbyDM9k6Rlisuk_yw_YSbt9p2V')
