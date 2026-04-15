<script lang="ts">
  import clsx from "clsx";
  import type { Field, Game } from "$lib/types/client-types";
  import type { ClassNameValue } from "tailwind-merge";

  const {
    game,
    field,
    className,
    onMount,
  }: {
    game: Game;
    field: Field;
    className?: {
      left?: ClassNameValue;
      right?: ClassNameValue;
    };
    onMount?: (leftEl: HTMLDivElement, rightEl: HTMLDivElement) => void;
  } = $props();

  let leftEl: HTMLDivElement;
  let rightEl: HTMLDivElement;

  $effect(() => {
    if (leftEl && rightEl) onMount?.(leftEl, rightEl);
  });
</script>

<div
  bind:this={leftEl}
  class={clsx(
    "absolute top-4 left-4 flex flex-col transition-opacity duration-75",
    className?.left,
  )}
>
  <p class="text-xs text-primary">MATCH_LOCATION</p>
  <h3 class="text-2xl text-primary font-semibold uppercase">
    {field.name.split(" ").join("_")}
  </h3>
  <div class="flex gap-2 items-center">
    <div class="flex bg-secondary items-center justify-center p-0.5 w-fit">
      <p class="text-[10px] text-primary">
        {#if field.orientation === "EW"}
          &lt;&gt; EW
        {:else}
          ^&#8964; NS
        {/if}
      </p>
    </div>
    <p class="text-[10px] text-primary opacity-70">
      {`LAT: ${field.min_lat}° N // LNG: ${field.min_lng}° E`}
    </p>
  </div>
</div>
<div
  bind:this={rightEl}
  class={clsx(
    "absolute top-4 right-4 flex flex-col text-end transition-opacity duration-75",
    className?.right,
  )}
>
  <div class="flex gap-2 items-center justify-end">
    <p class="text-xs text-primary">
      {`${game.my_team_score} - ${game.opponent_score}`}
    </p>
    <span class="text-xs text-primary">//</span>
    <p class="text-xs text-primary">
      {#if game.my_team_score !== null && game.opponent_score !== null}
        {#if game.my_team_score > game.opponent_score}
          WIN
        {:else if game.my_team_score < game.opponent_score}
          LOSS
        {:else}
          DRAW
        {/if}
      {/if}
    </p>
  </div>
  <h4 class="text-md text-primary font-semibold uppercase">
    {game.position?.split(" ").join("_")}
  </h4>
  <p class="text-xs text-primary">{game.created_at}</p>
</div>
