<script lang="ts">
  import Player from "./Player.svelte";
  import { doRectsOverlap, getRectWithBuffer } from "$lib/utils/rectangle.js";
  import Field from "$lib/components/Field.svelte";
  import MatchDetailInfo from "$lib/components/MatchDetailInfo.svelte";

  const { data } = $props();

  let fieldContainerHeight = $state<number>(0);
  let fieldContainerWidth = $state<number>(0);

  let playerEl = $state<HTMLDivElement>();
  let leftInfoEl = $state<HTMLDivElement>();
  let rightInfoEl = $state<HTMLDivElement>();
  let isLeftOverlapping = $state(false);
  let isRightOverlapping = $state(false);

  $effect(() => {
    if (!playerEl) return;

    const observer = new MutationObserver(() => {
      const playerRect = playerEl!.getBoundingClientRect();
      isLeftOverlapping = leftInfoEl
        ? doRectsOverlap(
            playerRect,
            getRectWithBuffer(leftInfoEl.getBoundingClientRect(), 60),
          )
        : false;
      isRightOverlapping = rightInfoEl
        ? doRectsOverlap(
            playerRect,
            getRectWithBuffer(rightInfoEl.getBoundingClientRect(), 60),
          )
        : false;
    });

    observer.observe(playerEl, {
      attributes: true,
      attributeFilter: ["style"],
    });
    return () => observer.disconnect();
  });
</script>

<div class="flex justify-center size-full">
  <section
    class="relative flex h-fit justify-center p-8 shadow-xl dark:shadow-lg dark:shadow-neutral-900 w-full max-w-200"
  >
    {#if data.game && data.field}
      <MatchDetailInfo
        game={data.game}
        field={data.field}
        onMount={(left, right) => {
          leftInfoEl = left;
          rightInfoEl = right;
        }}
        className={{
          left: isLeftOverlapping && "opacity-20",
          right: isRightOverlapping && "opacity-20",
        }}
      />
    {/if}

    <Field
      onMount={(h, w) => {
        fieldContainerHeight = h;
        fieldContainerWidth = w;
      }}
    >
      {#await data.positions}
        <span
          class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 font-semibold text-tertiary-500 text-2xl animate-pulse"
        >
          PLAYBACK_LOADING
        </span>
      {:then positionData}
        <Player
          {fieldContainerHeight}
          {fieldContainerWidth}
          {positionData}
          onMount={(el) => (playerEl = el)}
        />
      {/await}
    </Field>
  </section>
</div>
