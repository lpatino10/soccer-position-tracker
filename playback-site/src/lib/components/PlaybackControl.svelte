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

  let seekElement: HTMLDivElement;
  $effect(() => {
    seekElement.style.left = `${playbackState.currentFrame === 0 ? 0 : (playbackState.currentFrame / (playbackState.frameCount - 1)) * 100}%`;
  });

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
    class="flex bg-neutral/70 text-primary has-checked:bg-primary has-checked:text-neutral px-2 py-1 cursor-pointer text-xs has-disabled:cursor-default has-disabled:opacity-50"
  >
    {label}
    <input
      type="radio"
      name="playback-speed"
      id={`radio-${speed}`}
      value={speed}
      checked={speed === playbackState.speed}
      onchange={onSpeedChange}
      class="appearance-none"
      disabled={isLoading}
    />
  </label>
{/snippet}

<div class="flex flex-col bg-primary-600/40 gap-8 px-6 py-8 w-full">
  <div class="relative bg-primary h-1 w-full">
    <!-- This should ideally be an input with type range, but styling the seek element is a pain and this is just a side project. -->
    <div
      bind:this={seekElement}
      class="appearance-none absolute left-0 -top-2.5 bg-primary h-6 w-1 cursor-grab"
    ></div>
  </div>

  <div class="grid grid-cols-[1fr_auto_1fr] items-center w-full">
    <p class="self-start text-xs text-primary">
      {`FRAME: ${playbackState.currentFrame + 1}/${playbackState.frameCount}`}
    </p>
    <fieldset class="flex gap-3 col-2" disabled={isLoading}>
      <button
        class="cursor-pointer text-primary disabled:cursor-default disabled:opacity-50"
        aria-label="Start from beginning"
        onclick={onRestartPress}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="currentColor"
          height="24px"
          viewBox="0 -960 960 960"
          width="24px"
        >
          <path
            d="M220-240v-480h80v480h-80Zm520 0L380-480l360-240v480Zm-80-240Zm0 90v-180l-136 90 136 90Z"
          />
        </svg>
      </button>

      {#if playbackState.isPlaying}
        <button
          class="bg-primary p-3 text-neutral cursor-pointer disabled:cursor-default disabled:opacity-50 [clip-path:polygon(0_0,100%_0,100%_calc(100%-16px),calc(100%-16px)_100%,0_100%)]"
          aria-label="Pause"
          onclick={onPlayPausePress}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            height="24px"
            viewBox="0 -960 960 960"
            width="24px"
          >
            <path
              d="M520-200v-560h240v560H520Zm-320 0v-560h240v560H200Zm400-80h80v-400h-80v400Zm-320 0h80v-400h-80v400Zm0-400v400-400Zm320 0v400-400Z"
            />
          </svg>
        </button>
      {:else}
        <button
          class="bg-primary p-3 text-neutral cursor-pointer disabled:cursor-default disabled:opacity-50 [clip-path:polygon(0_0,100%_0,100%_calc(100%-16px),calc(100%-16px)_100%,0_100%)]"
          aria-label="Play"
          onclick={onPlayPausePress}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            height="24px"
            viewBox="0 -960 960 960"
            width="24px"
          >
            <path
              d="M320-200v-560l440 280-440 280Zm80-280Zm0 134 210-134-210-134v268Z"
            />
          </svg>
        </button>
      {/if}

      <!-- Space filler to get positioning right -->
      <div class="size-6"></div>
    </fieldset>

    <div class="flex flex-col gap-1 justify-self-end">
      <p class="text-[10px] text-primary">PLAYBACK_SPEED</p>
      <fieldset class="flex gap-1">
        {@render playbackSpeedButton(0.5, "0.5X")}
        {@render playbackSpeedButton(1, "1.0X")}
        {@render playbackSpeedButton(2, "2.0X")}
      </fieldset>
    </div>
  </div>
</div>
