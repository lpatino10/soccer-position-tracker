<script lang="ts">
  import MatchPlaybackScreen from "$lib/components/MatchPlaybackScreen.svelte";
  import {
    setPlaybackContext,
    type PlaybackSpeed,
    type PlaybackState,
  } from "$lib/context/playbackContext.js";
  import type { PositionData } from "$lib/types/api-types.js";

  const BASE_INTERVAL_DURATION = 100;

  const playbackState = $state<PlaybackState>({
    speed: 1,
    isPlaying: true,
    currentFrame: 0,
    frameCount: 1,
  });
  setPlaybackContext(playbackState);

  const { data } = $props();

  let intervalId: NodeJS.Timeout | undefined;
  let positionData = $state<Awaited<PositionData> | undefined>();

  $effect(() => {
    data.positions.then((resolved) => {
      positionData = resolved;
      playbackState.frameCount = resolved.length;
    });
  });

  function pausePlayback() {
    clearInterval(intervalId);
    intervalId = undefined;
  }

  function startPlayback(speed: PlaybackSpeed) {
    pausePlayback();

    if (!positionData) {
      return;
    }

    const positions = positionData;

    intervalId = setInterval(
      () => {
        playbackState.currentFrame += 1;
        if (playbackState.currentFrame >= positions.length) {
          playbackState.currentFrame = 0;
        }
      },
      (1 / speed) * BASE_INTERVAL_DURATION,
    );
  }

  $effect(() => {
    const speed = playbackState.speed;

    if (positionData && playbackState.isPlaying) {
      startPlayback(speed);
    } else {
      pausePlayback();
    }

    return () => {
      clearInterval(intervalId);
    };
  });
</script>

{#if data.game && data.field}
  <MatchPlaybackScreen
    game={data.game}
    field={data.field}
    positions={data.positions}
  />
{/if}
