<script lang="ts">
  import MatchLogItem from "./MatchLogItem.svelte";
  import type { load } from "../../routes/+page.server";

  interface Props {
    matchLogData: Awaited<ReturnType<typeof load>>;
  }

  const { matchLogData }: Props = $props();
</script>

<ol class="size-full divide-y divide-neutral-200 dark:divide-neutral-500">
  {#each matchLogData.data as { created_at, id, field_id, position, my_team_score, opponent_score }}
    <MatchLogItem
      {created_at}
      {id}
      {field_id}
      {position}
      my_team_score={my_team_score || 0}
      opponent_score={opponent_score || 0}
    />
  {/each}
</ol>
