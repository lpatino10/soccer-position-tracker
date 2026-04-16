<script lang="ts">
  type PlaybackSpeed = 0.5 | 1 | 2;

  // TODO: Move to context.
  let playbackSpeed = $state<PlaybackSpeed>(1);
  let isPlaying = $state<boolean>(false);

  function onSpeedChange(event: Event) {
    const target = event.target as HTMLInputElement;
    playbackSpeed = Number(target.value) as PlaybackSpeed;
  }
</script>

{#snippet playbackSpeedButton(speed: PlaybackSpeed, label: string)}
  <label
    for={`radio-${speed}`}
    class="flex bg-neutral/70 text-primary has-checked:bg-primary has-checked:text-neutral px-2 py-1 cursor-pointer text-xs"
  >
    {label}
    <input
      type="radio"
      name="playback-speed"
      id={`radio-${speed}`}
      value={speed}
      checked={speed === playbackSpeed}
      onchange={onSpeedChange}
      class="appearance-none"
    />
  </label>
{/snippet}

<div class="flex flex-col bg-primary-600/40 gap-8 px-6 py-8 w-full">
  <div class="relative bg-primary h-1 w-full">
    <div class="absolute left-0 -top-2.5 bg-primary h-6 w-1 cursor-grab"></div>
  </div>

  <div class="grid grid-cols-[1fr_auto_1fr] items-center w-full">
    <fieldset class="flex gap-3 col-2">
      <button class="cursor-pointer" aria-label="Start from beginning">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="24px"
          viewBox="0 -960 960 960"
          width="24px"
          fill="#e3e3e3"
        >
          <path
            d="M220-240v-480h80v480h-80Zm520 0L380-480l360-240v480Zm-80-240Zm0 90v-180l-136 90 136 90Z"
          />
        </svg>
      </button>
      {#if isPlaying}
        <button
          class="bg-primary p-3 text-neutral cursor-pointer [clip-path:polygon(0_0,100%_0,100%_calc(100%-16px),calc(100%-16px)_100%,0_100%)]"
          aria-label="Pause"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
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
          class="bg-primary p-3 text-neutral cursor-pointer [clip-path:polygon(0_0,100%_0,100%_calc(100%-16px),calc(100%-16px)_100%,0_100%)]"
          aria-label="Play"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
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
