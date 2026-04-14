<script lang="ts">
  import Player from "./Player.svelte";

  const { data } = $props();

  let fieldContainerHeight = $state<number>(0);
  let fieldContainerWidth = $state<number>(0);
</script>

<div class="flex justify-center size-full">
  <section class="flex justify-center p-4 w-full">
    <div
      bind:clientHeight={fieldContainerHeight}
      bind:clientWidth={fieldContainerWidth}
      class="flex relative border border-primary aspect-110/70 h-fit w-full max-w-200 overflow-hidden after:content-[''] after:bg-primary after:h-full after:w-px after:absolute after:left-1/2 after:-translate-x-1/2"
    >
      <!-- Left penalty box -->
      <div
        class="absolute h-[63%] w-[16.4%] border border-l-0 border-primary top-[18.5%] z-10 bg-neutral"
      ></div>
      <div
        class="absolute h-[29%] w-[5.5%] border border-l-0 border-primary top-[35.5%] z-10"
      ></div>
      <div
        class="absolute bg-primary size-1 rounded-full top-1/2 left-[11%] -translate-1/2 z-10 md:size-1.5"
      ></div>
      <div
        class="absolute top-1/2 left-[11%] -translate-1/2 h-2/7 aspect-square border border-primary rounded-full"
      ></div>

      <!-- Center circle -->
      <div
        class="relative h-2/7 aspect-square border border-primary rounded-full left-1/2 top-1/2 -translate-1/2"
      >
        <div
          class="absolute bg-primary size-1 rounded-full left-1/2 top-1/2 -translate-1/2 md:size-1.5"
        ></div>
      </div>

      <!-- Right penalty box -->
      <div
        class="absolute h-[63%] w-[16.4%] border border-r-0 border-primary top-[18.5%] right-0 z-10 bg-neutral"
      ></div>
      <div
        class="absolute h-[29%] w-[5.5%] border border-r-0 border-primary top-[35.5%] right-0 z-10"
      ></div>
      <div
        class="absolute bg-primary size-1 rounded-full top-1/2 right-[11%] translate-x-1/2 -translate-y-1/2 z-10 md:size-1.5"
      ></div>
      <div
        class="absolute top-1/2 right-[11%] translate-x-1/2 -translate-y-1/2 h-2/7 aspect-square border border-primary rounded-full"
      ></div>

      <!-- Corners -->
      <div
        class="absolute top-0 left-0 h-3 aspect-square rounded-full border border-primary -translate-1/2 md:h-4"
      ></div>
      <div
        class="absolute top-0 right-0 h-3 aspect-square rounded-full border border-primary translate-x-1/2 -translate-y-1/2 md:h-4"
      ></div>
      <div
        class="absolute bottom-0 left-0 h-3 aspect-square rounded-full border border-primary -translate-x-1/2 translate-y-1/2 md:h-4"
      ></div>
      <div
        class="absolute bottom-0 right-0 h-3 aspect-square rounded-full border border-primary translate-1/2 md:h-4"
      ></div>

      {#await data.positions}
        <div
          class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-gray-700 flex items-center justify-center p-1 rounded-md"
        >
          <span class="font-semibold text-gray-200 animate-pulse">
            Loading playback...
          </span>
        </div>
      {:then positionData}
        <Player {fieldContainerHeight} {fieldContainerWidth} {positionData} />
      {/await}
    </div>
  </section>
  {#if data.game}
    <div class="flex flex-col gap-2">
      {#if data.field}
        <p>{data.field.name}</p>
      {/if}
      <div class="flex gap-2 items-center">
        {#if data.game.my_team_score !== null && data.game.opponent_score !== null}
          {#if data.game.my_team_score > data.game.opponent_score}
            <span class="font-bold text-green-700">W</span>
          {:else if data.game.my_team_score < data.game.opponent_score}
            <span class="font-bold text-red-700">L</span>
          {:else}
            <span class="font-bold">D</span>
          {/if}
        {/if}
        {data.game.my_team_score} - {data.game.opponent_score}
      </div>
      <p>{data.game.position}</p>
    </div>
  {/if}
</div>
