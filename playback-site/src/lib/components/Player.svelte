<script lang="ts">
  import { getPlaybackState } from "$lib/context/playbackContext";
  import type { PositionData } from "$lib/types/api-types";

  interface Props {
    fieldContainerHeight: number;
    fieldContainerWidth: number;
    positionData: PositionData;
    onMount?: (el: HTMLDivElement) => void;
  }

  const {
    fieldContainerHeight,
    fieldContainerWidth,
    positionData,
    onMount,
  }: Props = $props();
  const playbackState = getPlaybackState();

  let playerElement: HTMLDivElement;

  $effect(() => {
    if (playerElement) onMount?.(playerElement);
  });

  $effect(() => {
    const currentPosition = positionData[playbackState.currentFrame];

    // - 4px to center dot
    playerElement.style.left = `${currentPosition.x * fieldContainerWidth - 4}px`;
    playerElement.style.top = `${currentPosition.y * fieldContainerHeight - 4}px`;
  });
</script>

<div
  bind:this={playerElement}
  class="absolute transition-all bg-tertiary size-2 rounded-full z-50"
></div>
