<script lang="ts">
  import Player from "./Player.svelte";

  const { data } = $props();

  let fieldContainerHeight = $state<number>(0);
  let fieldContainerWidth = $state<number>(0);
</script>

<div class="flex justify-center size-full">
  <section
    class="relative flex h-fit justify-center p-8 shadow-xl dark:shadow-lg dark:shadow-neutral-900 w-full max-w-200"
  >
    <!-- Match info -->
    {#if data.game}
      {#if data.field}
        <div class="absolute top-4 left-4 flex flex-col">
          <p class="text-xs text-primary">MATCH_LOCATION</p>
          <h3 class="text-2xl text-primary font-semibold uppercase">
            {data.field.name.split(" ").join("_")}
          </h3>
          <div class="flex gap-2 items-center">
            <div
              class="flex bg-secondary items-center justify-center p-0.5 w-fit"
            >
              <p class="text-[10px] text-primary">
                {#if data.field.orientation === "EW"}
                  &lt;&gt; EW
                {:else}
                  ^&#8964; NS
                {/if}
              </p>
            </div>
            <p class="text-[10px] text-primary opacity-70">
              {`LAT: ${data.field.min_lat}° N // LNG: ${data.field.min_lng}° E`}
            </p>
          </div>
        </div>
        <div class="absolute top-4 right-4 flex flex-col text-end">
          <div class="flex gap-2 items-center justify-end">
            <p class="text-xs text-primary">
              {`${data.game.my_team_score} - ${data.game.opponent_score}`}
            </p>
            <span class="text-xs text-primary">//</span>
            <p class="text-xs text-primary">
              {#if data.game.my_team_score !== null && data.game.opponent_score !== null}
                {#if data.game.my_team_score > data.game.opponent_score}
                  WIN
                {:else if data.game.my_team_score < data.game.opponent_score}
                  LOSS
                {:else}
                  DRAW
                {/if}
              {/if}
            </p>
          </div>
          <h4 class="text-md text-primary font-semibold uppercase">
            {data.game.position?.split(" ").join("_")}
          </h4>
          <p class="text-xs text-primary">{data.game.created_at}</p>
        </div>
      {/if}
    {/if}

    <div
      bind:clientHeight={fieldContainerHeight}
      bind:clientWidth={fieldContainerWidth}
      class="flex relative border border-primary aspect-110/70 h-fit w-full overflow-hidden after:content-[''] after:bg-primary after:h-full after:w-px after:absolute after:left-1/2 after:-translate-x-1/2"
    >
      <!-- Left penalty box -->
      <div
        class="absolute h-[63%] w-[16.4%] border border-l-0 border-primary top-[18.5%] z-10 bg-neutral"
      ></div>
      <div
        class="absolute h-[29%] w-[5.5%] border border-l-0 border-primary top-[35.5%] z-10"
      ></div>
      <div
        class="absolute bg-primary size-1 rounded-full top-1/2 left-[11%] -translate-1/2 z-10"
      ></div>
      <div
        class="absolute top-1/2 left-[11%] -translate-1/2 h-2/7 aspect-square border border-primary rounded-full"
      ></div>

      <!-- Center circle -->
      <div
        class="relative h-2/7 aspect-square border border-primary rounded-full left-1/2 top-1/2 -translate-1/2"
      >
        <div
          class="absolute bg-primary size-1 rounded-full left-1/2 top-1/2 -translate-1/2"
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
        class="absolute bg-primary size-1 rounded-full top-1/2 right-[11%] translate-x-1/2 -translate-y-1/2 z-10"
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
        <span
          class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 font-semibold text-tertiary-500 text-2xl animate-pulse"
        >
          PLAYBACK_LOADING
        </span>
      {:then positionData}
        <Player {fieldContainerHeight} {fieldContainerWidth} {positionData} />
      {/await}
    </div>
  </section>
</div>
