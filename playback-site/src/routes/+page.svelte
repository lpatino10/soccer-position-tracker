<script lang="ts">
  import MatchLogHeader from "$lib/components/MatchLogHeader.svelte";
  import MatchLogList from "$lib/components/MatchLogList.svelte";
  const { data } = $props();
</script>

<MatchLogHeader totalMatches={data.data?.length || 0} />
<div class="h-4"></div>
<MatchLogList matchLogData={data} />
