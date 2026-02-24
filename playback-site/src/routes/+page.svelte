<script lang="ts">
  const { data } = $props();
</script>

<h1 class="text-3xl pb-3">Games</h1>
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
