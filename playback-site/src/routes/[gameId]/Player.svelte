<script lang="ts">
  import type { PositionData } from "$lib/api-types";

  const { positionData }: { positionData: PositionData } = $props();
  let dataIndex = $state(0);

  let playerElement: HTMLDivElement;

  $effect(() => {
    setInterval(() => {
      const position = positionData[dataIndex];

      playerElement.style.left = `${position.x * 590}px`;
      playerElement.style.top = `${position.y * 380}px`;

      dataIndex += 1;
      if (dataIndex >= positionData.length) {
        dataIndex = 0;
      }
    }, 100);
  });
</script>

<div
  bind:this={playerElement}
  class="absolute transition-all bg-yellow-300 size-2 rounded-full"
></div>
