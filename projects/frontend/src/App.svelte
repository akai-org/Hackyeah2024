<script>
import Home from "./pages/Home.svelte";
import Login from "./pages/Login.svelte";
import { onMount } from "svelte";

let messages = $state([]);
let page = $state(1);

onMount(() => {
  messages.push({
    id: 0,
    owner: "user",
    // Unix timestamp in ms
    time: "1727535900743",
    text: "Lorem ipsum dolor sit amet, qui minim labore adipisicing minim sint cillum sint consectetur cupidatat.",
  });

  messages.push({
    id: 0,
    owner: "server",
    // Unix timestamp in ms
    time: "1727537900743",
    text: "Lorem ipsum dolor sit amet, officia excepteur ex fugiat reprehenderit enim labore culpa sint ad nisi Lorem pariatur mollit ex esse exercitation amet. Nisi anim cupidatat excepteur officia. Reprehenderit nostrud nostrud ipsum Lorem est aliquip amet voluptate voluptate dolor minim nulla est proident. Nostrud officia pariatur ut officia. Sit irure elit esse ea nulla sunt ex occaecat reprehenderit commodo officia dolor Lorem duis laboris cupidatat officia voluptate. Culpa proident adipisicing id nulla nisi laboris ex in Lorem sunt duis officia eiusmod. Aliqua reprehenderit commodo ex non excepteur duis sunt velit enim. Voluptate laboris sint cupidatat ullamco ut ea consectetur et est culpa et culpa duis.",
  });
});
</script>

{#if page === 0}
  <Login bind:page /> 
{:else}
  <Home />
{/if}

<style>
</style>
