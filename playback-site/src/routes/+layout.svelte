<script lang="ts">
	import "../app.css";
	import favicon from "$lib/assets/favicon.svg";
	import ThemeToggle from "$lib/components/ThemeToggle.svelte";

	let { children } = $props();
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<div class="bg-neutral h-dvh w-full">
	<div
		class="border-b border-neutral-200 flex items-center justify-between px-4 py-3"
	>
		<h1 class="font-semibold text-primary text-3xl">MATCH_REPLAY</h1>
		<ThemeToggle />
	</div>
	{@render children()}
</div>
