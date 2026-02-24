<script lang="ts">
  const { data } = $props();
</script>

<ul>
  {#each data.data as event}
    <li>({event.lat}, {event.lng})</li>
  {/each}
</ul>
