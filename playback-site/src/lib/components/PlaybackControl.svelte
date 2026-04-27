<script lang="ts">
  import {
    getPlaybackState,
    type PlaybackSpeed,
  } from "$lib/context/playbackContext";

  interface Props {
    isLoading: boolean;
  }

  const { isLoading }: Props = $props();
  const playbackState = getPlaybackState();

  function onSeek(event: Event) {
    const target = event.target as HTMLInputElement;
    playbackState.currentFrame = Number(target.value);
  }

  function onSpeedChange(event: Event) {
    const target = event.target as HTMLInputElement;
    playbackState.speed = Number(target.value) as PlaybackSpeed;
  }

  function onPlayPausePress() {
    playbackState.isPlaying = !playbackState.isPlaying;
  }

  function onRestartPress() {
    playbackState.currentFrame = 0;
  }
</script>

{#snippet playbackSpeedButton(speed: PlaybackSpeed, label: string)}
  <label
    for={`radio-${speed}`}
    class="flex bg-neutral/70 text-primary has-checked:bg-primary has-checked:text-neutral px-1 sm:px-2 py-0.5 sm:py-1 cursor-pointer text-[10px] sm:text-xs has-disabled:cursor-default has-disabled:opacity-50"
  >
    {label}
    <input
      type="radio"
      name="playback-speed"
      id={`radio-${speed}`}
      value={speed}
      checked={speed === playbackState.speed}
      onchange={onSpeedChange}
      class="appearance-none size-0"
      disabled={isLoading}
    />
  </label>
{/snippet}

<div class="flex flex-col bg-primary-600/40 gap-8 px-6 py-8 w-full">
  <input
    class="appearance-none bg-transparent w-full"
    oninput={onSeek}
    type="range"
    min="0"
    max={`${playbackState.frameCount - 1}`}
    value={`${playbackState.currentFrame}`}
  />

  <div class="grid grid-cols-[1fr_auto_1fr] items-center w-full">
    <div
      class="flex flex-col self-start sm:flex-row sm:gap-1 min-w-0 text-[10px] sm:text-xs text-primary"
    >
      <p>FRAME:</p>
      <p>
        {`${playbackState.currentFrame + 1}/${playbackState.frameCount}`}
      </p>
    </div>

    <fieldset class="flex gap-3 col-2 items-center" disabled={isLoading}>
      <button
        class="cursor-pointer text-primary size-4 sm:size-6 disabled:cursor-default disabled:opacity-50"
        aria-label="Start from beginning"
        onclick={onRestartPress}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="currentColor"
          viewBox="0 -960 960 960"
        >
          <path
            d="M220-240v-480h80v480h-80Zm520 0L380-480l360-240v480Zm-80-240Zm0 90v-180l-136 90 136 90Z"
          />
        </svg>
      </button>

      {#if playbackState.isPlaying}
        <button
          class="bg-primary p-2 sm:p-3 text-neutral size-8 sm:size-12 cursor-pointer disabled:cursor-default disabled:opacity-50 [clip-path:polygon(0_0,100%_0,100%_calc(100%-12px),calc(100%-12px)_100%,0_100%)] sm:[clip-path:polygon(0_0,100%_0,100%_calc(100%-16px),calc(100%-16px)_100%,0_100%)]"
          aria-label="Pause"
          onclick={onPlayPausePress}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            viewBox="0 -960 960 960"
          >
            <path
              d="M520-200v-560h240v560H520Zm-320 0v-560h240v560H200Zm400-80h80v-400h-80v400Zm-320 0h80v-400h-80v400Zm0-400v400-400Zm320 0v400-400Z"
            />
          </svg>
        </button>
      {:else}
        <button
          class="bg-primary p-2 sm:p-3 text-neutral size-8 sm:size-12 cursor-pointer disabled:cursor-default disabled:opacity-50 [clip-path:polygon(0_0,100%_0,100%_calc(100%-12px),calc(100%-12px)_100%,0_100%)] sm:[clip-path:polygon(0_0,100%_0,100%_calc(100%-16px),calc(100%-16px)_100%,0_100%)]"
          aria-label="Play"
          onclick={onPlayPausePress}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            viewBox="0 -960 960 960"
          >
            <path
              d="M320-200v-560l440 280-440 280Zm80-280Zm0 134 210-134-210-134v268Z"
            />
          </svg>
        </button>
      {/if}

      <!-- Space filler to get positioning right -->
      <div class="size-4 sm:size-6"></div>
    </fieldset>

    <div class="flex flex-col gap-1 justify-self-end min-w-0">
      <p class="text-[6px] sm:text-[10px] text-primary">PLAYBACK_SPEED</p>
      <fieldset class="flex gap-1 min-w-0">
        {@render playbackSpeedButton(0.5, "0.5X")}
        {@render playbackSpeedButton(1, "1.0X")}
        {@render playbackSpeedButton(2, "2.0X")}
      </fieldset>
    </div>
  </div>
</div>

<style>
  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
  }

  input[type="range"]:focus {
    outline: none;
  }

  input[type="range"]::-ms-track {
    width: 100%;
    cursor: pointer;
    background: transparent;
    border-color: transparent;
    color: transparent;
  }

  /* Special styling for WebKit/Blink */
  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    height: 24px;
    width: 6px;
    background: var(--color-primary);
    cursor: pointer;
    margin-top: -10px; /* You need to specify a margin in Chrome, but in Firefox and IE it is automatic */
  }

  /* All the same stuff for Firefox */
  input[type="range"]::-moz-range-thumb {
    height: 24px;
    width: 6px;
    background: var(--color-primary);
    cursor: pointer;
  }

  /* All the same stuff for IE */
  input[type="range"]::-ms-thumb {
    height: 24px;
    width: 6px;
    background: var(--color-primary);
    cursor: pointer;
  }

  input[type="range"]::-webkit-slider-runnable-track {
    width: 100%;
    height: 4px;
    cursor: pointer;
    background: var(--color-primary);
  }

  input[type="range"]::-moz-range-track {
    width: 100%;
    height: 4px;
    cursor: pointer;
    background: var(--color-primary);
  }

  input[type="range"]::-ms-track {
    width: 100%;
    height: 4px;
    cursor: pointer;
    background: transparent;
    border-color: transparent;
    color: transparent;
  }

  input[type="range"]::-ms-fill-lower {
    background: var(--color-primary);
  }

  input[type="range"]::-ms-fill-upper {
    background: var(--color-primary);
  }
</style>
