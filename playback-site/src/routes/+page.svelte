<script lang="ts">
  const { data } = $props();

  const currentDate = new Date();
  const lastSync = `${currentDate.getFullYear()}.${currentDate.getMonth()}.${currentDate.getDate()}_${currentDate.getHours()}:${currentDate.getMinutes()}`;
</script>

<div class="flex justify-between py-3">
  <div class="flex flex-col gap-1">
    <div class="bg-secondary px-1 py-0.5 w-fit">
      <p class="text-headline text-[10px]">DATA_STREAM</p>
    </div>
    <h1 class="font-semibold text-primary text-6xl">MATCH_LOG</h1>
  </div>
  <div class="flex flex-col items-end justify-end">
    <p class="font-light text-body text-xs">
      {`RECORDS_FOUND: ${data.data?.length || 0}`}
    </p>
    <p class="font-light text-body text-xs">
      {`LAST_SYNC: ${lastSync}`}
    </p>
    <p class="text-primary text-xs">// REPLAY_ENGINE_ACTIVE</p>
  </div>
</div>
<ul>
  {#each data.data as { created_at, id, position, my_team_score, opponent_score }}
    <a href="/{id}">
      <li>
        <div
          class="flex flex-col border border-gray-500 rounded-md px-2 py-1 w-fit"
        >
          <span class="text-xs"
            >{new Date(created_at).toLocaleDateString()}</span
          >
          <div>
            <span class="font-semibold">{my_team_score} - {opponent_score}</span
            >
            <span> | {position}</span>
          </div>
        </div>
      </li>
    </a>
  {/each}
</ul>
