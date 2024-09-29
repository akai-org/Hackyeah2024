<script>
import Home from "./pages/Home.svelte";
import Login from "./pages/Login.svelte";
import { onMount } from "svelte";

let messages = $state([]);
let page = $state(0);

onMount(() => {
});
</script>

{#if page === 0}
  <Login bind:page /> 
{:else}
  <Home />
{/if}

<style>
</style>

