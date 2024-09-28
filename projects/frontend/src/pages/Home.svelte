<script>
import Chat from "../components/chat/Chat.svelte";
import { onMount } from "svelte";
import { messageStore } from "../libs/webSocket.js";

let { messages } = $props();
let error = $state();

onMount(() => {
  messageStore.subscribe(msg => {
    if (msg.connected === false) {
      // TODO: ENABLE
      // error = true;
    }
  });
});
</script>

{#if error === true}
  <div id="error">
    <h1>ERROR</h1>
  </div>
{/if}

<div class="main">
  <div></div>

  <div>
    <Chat />
  </div>

  <div></div>
</div>

<style>
#error {
  position: absolute;
  height: 100vh;
  width: 100vw;
  background-color: #f00;
  display: flex;
}

#error h1 {
  margin: auto;
  font-size: 5rem;
  color: #fff;
}
.main {
  height: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
}
</style>
