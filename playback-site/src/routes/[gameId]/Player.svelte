<script lang="ts">
  import type { PositionData } from "$lib/api-types";

  const { positionData }: { positionData: PositionData } = $props();
  let dataIndex = $state(0);

  let playerElement: HTMLDivElement;

  $effect(() => {
    const interval = setInterval(() => {
      const position = positionData[dataIndex];

      // 20px border outside field boundaries, so we need to account for that.
      playerElement.style.left = `${position.x * 550 + 20}px`;
      playerElement.style.top = `${position.y * 340 + 20}px`;

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
  class="absolute transition-all bg-yellow-300 size-2 rounded-full"
></div>
