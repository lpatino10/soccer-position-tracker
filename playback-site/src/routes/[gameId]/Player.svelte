<script lang="ts">
  import type { GameData } from "$lib/api-types";

  const { gameData }: { gameData: GameData } = $props();
  let dataIndex = $state(0);

  let playerElement: HTMLDivElement;

  $effect(() => {
    setInterval(() => {
      const position = gameData[dataIndex];

      playerElement.style.left = `${position.x * 590}px`;
      playerElement.style.top = `${position.y * 380}px`;

      dataIndex += 1;
      if (dataIndex >= gameData.length) {
        dataIndex = 0;
      }
    }, 100);
  });
</script>

<div
  bind:this={playerElement}
  class="absolute transition-all bg-yellow-300 size-2 rounded-full"
></div>
