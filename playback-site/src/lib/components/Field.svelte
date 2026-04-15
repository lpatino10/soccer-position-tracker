<script lang="ts">
  import type { Snippet } from "svelte";

  const {
    onMount,
    children,
  }: { onMount?: (height: number, width: number) => void; children: Snippet } =
    $props();

  let fieldHeight = $state<number>(0);
  let fieldWidth = $state<number>(0);

  $effect(() => {
    onMount?.(fieldHeight, fieldWidth);
  });
</script>

<div
  bind:clientHeight={fieldHeight}
  bind:clientWidth={fieldWidth}
  class="flex relative border border-primary aspect-110/70 h-fit w-full overflow-hidden after:content-[''] after:bg-primary after:h-full after:w-px after:absolute after:left-1/2 after:-translate-x-1/2"
>
  <!-- Left penalty box -->
  <div
    class="absolute h-[63%] w-[16.4%] border border-l-0 border-primary top-[18.5%] z-10 bg-neutral"
  ></div>
  <div
    class="absolute h-[29%] w-[5.5%] border border-l-0 border-primary top-[35.5%] z-10"
  ></div>
  <div
    class="absolute bg-primary size-1 rounded-full top-1/2 left-[11%] -translate-1/2 z-10"
  ></div>
  <div
    class="absolute top-1/2 left-[11%] -translate-1/2 h-2/7 aspect-square border border-primary rounded-full"
  ></div>

  <!-- Center circle -->
  <div
    class="relative h-2/7 aspect-square border border-primary rounded-full left-1/2 top-1/2 -translate-1/2"
  >
    <div
      class="absolute bg-primary size-1 rounded-full left-1/2 top-1/2 -translate-1/2"
    ></div>
  </div>

  <!-- Right penalty box -->
  <div
    class="absolute h-[63%] w-[16.4%] border border-r-0 border-primary top-[18.5%] right-0 z-10 bg-neutral"
  ></div>
  <div
    class="absolute h-[29%] w-[5.5%] border border-r-0 border-primary top-[35.5%] right-0 z-10"
  ></div>
  <div
    class="absolute bg-primary size-1 rounded-full top-1/2 right-[11%] translate-x-1/2 -translate-y-1/2 z-10"
  ></div>
  <div
    class="absolute top-1/2 right-[11%] translate-x-1/2 -translate-y-1/2 h-2/7 aspect-square border border-primary rounded-full"
  ></div>

  <!-- Corners -->
  <div
    class="absolute top-0 left-0 h-3 aspect-square rounded-full border border-primary -translate-1/2 md:h-4"
  ></div>
  <div
    class="absolute top-0 right-0 h-3 aspect-square rounded-full border border-primary translate-x-1/2 -translate-y-1/2 md:h-4"
  ></div>
  <div
    class="absolute bottom-0 left-0 h-3 aspect-square rounded-full border border-primary -translate-x-1/2 translate-y-1/2 md:h-4"
  ></div>
  <div
    class="absolute bottom-0 right-0 h-3 aspect-square rounded-full border border-primary translate-1/2 md:h-4"
  ></div>

  {@render children()}
</div>
