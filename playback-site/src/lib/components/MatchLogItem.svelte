<script lang="ts">
  import { cn } from "$lib/utils/cn";

  interface Props {
    created_at: string;
    id: string;
    field_id: number | null;
    position: string | null;
    my_team_score: number;
    opponent_score: number;
  }

  const {
    created_at,
    id,
    field_id = 0,
    position,
    my_team_score,
    opponent_score,
  }: Props = $props();

  let result: "win" | "loss" | "draw" = $derived.by(() => {
    if (my_team_score > opponent_score) {
      return "win";
    } else if (my_team_score < opponent_score) {
      return "loss";
    } else {
      return "draw";
    }
  });
</script>

{#snippet resultBadge(result: "win" | "loss" | "draw")}
  <div
    class={cn(
      "px-1.5 sm:px-2 py-0.5 sm:py-1",
      result === "win" && "bg-primary text-[#F9F7E8] dark:text-neutral",
      result === "loss" && "bg-orange-600 text-[#F9F7E8]",
      result === "draw" && "bg-neutral-900 text-[#F9F7E8]",
    )}
  >
    <p class="text-[10px] sm:text-xs">
      {result === "win" ? "WIN" : result === "loss" ? "LOSS" : "DRAW"}
    </p>
  </div>
{/snippet}

<li>
  <div class="group flex py-2 w-full">
    <div class="relative w-1 shrink-0">
      <div class="absolute inset-0 bg-neutral-400"></div>
      <div
        class="absolute inset-0 bg-primary transition-[clip-path] duration-300 [clip-path:inset(0_0_100%_0)] group-hover:[clip-path:inset(0_0_0_0)]"
      ></div>
    </div>

    <div class="flex flex-col px-2 sm:px-3 pb-2.5 sm:py-4 w-full">
      <div class="flex sm:hidden items-center gap-2 pb-1.5">
        <p class="text-primary text-[8px] sm:text-[10px]">{`F_0${field_id}`}</p>
        <p class="text-[8px] sm:text-[10px] text-body/80">{created_at}</p>
      </div>
      <div class="flex items-center justify-between">
        <div class="hidden sm:flex flex-col">
          <p class="text-primary text-xs">{`//F_0${field_id}`}</p>
          <p class="text-sm">{created_at}</p>
        </div>

        <div class="flex gap-5 items-center">
          <h3 class="text-sm sm:text-2xl">MENACE FC</h3>
          <div class="flex flex-col items-center">
            <h3 class="font-semibold text-xs sm:text-xl">
              {`${my_team_score} - ${opponent_score}`}
            </h3>
            {@render resultBadge(result)}
          </div>
          <h3 class="text-sm sm:text-2xl">OPPONENT</h3>
        </div>

        <a
          href={`/${id}`}
          class="bg-primary cursor-pointer px-3 sm:px-5 py-2 sm:py-3 text-xs sm:text-sm text-neutral [clip-path:polygon(0_0,100%_0,100%_calc(100%-12px),calc(100%-12px)_100%,0_100%)] sm:[clip-path:polygon(0_0,100%_0,100%_calc(100%-16px),calc(100%-16px)_100%,0_100%)] hover:bg-secondary hover:text-headline"
        >
          VIEW REPLAY
        </a>
      </div>
    </div>
  </div>
</li>
