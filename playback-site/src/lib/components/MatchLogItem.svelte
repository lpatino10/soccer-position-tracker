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
      "px-2 py-1",
      result === "win" && "bg-primary text-[#F9F7E8] dark:text-neutral",
      result === "loss" && "bg-orange-600 text-[#F9F7E8]",
      result === "draw" && "bg-neutral-900 text-[#F9F7E8]",
    )}
  >
    <p class="text-xs">
      {result === "win" ? "WIN" : result === "loss" ? "LOSS" : "DRAW"}
    </p>
  </div>
{/snippet}

<li>
  <div class="group flex relative w-full">
    <div class="bg-neutral-400 h-full w-1"></div>
    <div
      class="absolute h-full w-1 bg-primary transition-all duration-300 scale-0 origin-top group-hover:scale-100"
    ></div>

    <div class="flex items-center justify-between px-3 py-4 w-full">
      <div class="flex flex-col">
        <p class="text-primary text-xs">{`//F_0${field_id}`}</p>
        <p class="text-sm">{created_at}</p>
      </div>

      <div class="flex gap-5 items-center">
        <h3 class="text-2xl">MENACE FC</h3>
        <div class="flex flex-col items-center">
          <h3 class="font-semibold text-xl">
            {`${my_team_score} - ${opponent_score}`}
          </h3>
          {@render resultBadge(result)}
        </div>
        <h3 class="text-2xl">OPPONENT</h3>
      </div>

      <a
        href={`/${id}`}
        class="bg-primary cursor-pointer px-5 py-3 text-sm text-neutral [clip-path:polygon(0_0,100%_0,100%_calc(100%-16px),calc(100%-16px)_100%,0_100%)] hover:bg-secondary hover:text-headline"
      >
        VIEW REPLAY
      </a>
    </div>
  </div>
</li>
