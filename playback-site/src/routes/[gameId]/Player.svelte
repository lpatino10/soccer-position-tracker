<script lang="ts">
  import type { PositionData } from "$lib/types/api-types";

  const {
    fieldContainerHeight,
    fieldContainerWidth,
    positionData,
    onMount,
  }: {
    fieldContainerHeight: number;
    fieldContainerWidth: number;
    positionData: PositionData;
    onMount?: (el: HTMLDivElement) => void;
  } = $props();
  let dataIndex = $state(0);

  let playerElement: HTMLDivElement;

  $effect(() => {
    if (playerElement) onMount?.(playerElement);
  });

  $effect(() => {
    const interval = setInterval(() => {
      const position = positionData[dataIndex];

      // Subtract 4px to center dot.
      playerElement.style.left = `${position.x * fieldContainerWidth - 4}px`;
      playerElement.style.top = `${position.y * fieldContainerHeight - 4}px`;

      dataIndex += 1;
      if (dataIndex >= positionData.length) {
        dataIndex = 0;
      }
    }, 100);

    return () => {
      clearInterval(interval);
    };
  });
</script>

<div
  bind:this={playerElement}
  class="absolute transition-all bg-tertiary size-2 rounded-full"
></div>
