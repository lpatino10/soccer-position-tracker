<script lang="ts">
	import "../app.css";
	import favicon from "$lib/assets/favicon.svg";
	import ThemeToggle from "$lib/components/ThemeToggle.svelte";
	import { version } from "$app/environment";

	let { children } = $props();
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<div class="bg-neutral flex flex-col h-dvh w-full">
	<div
		class="border-b border-neutral-200 dark:border-neutral-500 flex items-center justify-between px-4 py-3"
	>
		<h2 class="font-semibold text-primary text-3xl">MATCH_REPLAY</h2>
		<ThemeToggle />
	</div>
	<div class="p-4 flex flex-1 flex-col">
		{@render children()}
	</div>
	<div
		class="border-t border-neutral-200 dark:border-neutral-500 flex items-center justify-between px-4 py-3"
	>
		<p class="text-body text-sm">{`VER: ${version}`}</p>
	</div>
	<div
		class="absolute rotate-90 right-0 bottom-0 origin-top-right -translate-x-1 text-body/25 whitespace-nowrap"
	>
		STATUS: ONLINE // LOGS: VERIFIED // POSITIONAL_DATA: SYNCED
	</div>
</div>
