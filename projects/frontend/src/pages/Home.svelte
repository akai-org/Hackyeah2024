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
  <div>
    <Chat />
  </div>

  <div class="tutorial">
    <h2>Tutorial</h2>

    <p>Lorem ipsum dolor sit amet, officia excepteur ex fugiat reprehenderit enim labore culpa sint ad nisi Lorem pariatur mollit ex esse exercitation amet. Nisi anim cupidatat excepteur officia. Reprehenderit nostrud nostrud ipsum Lorem est aliquip amet voluptate voluptate dolor minim nulla est proident. Nostrud officia pariatur ut officia. Sit irure elit esse ea nulla sunt ex occaecat reprehenderit commodo officia dolor Lorem duis laboris cupidatat officia voluptate. Culpa proident adipisicing id nulla nisi laboris ex in Lorem sunt duis officia eiusmod. Aliqua reprehenderit commodo ex non excepteur duis sunt velit enim. Voluptate laboris sint cupidatat ullamco ut ea consectetur et est culpa et culpa duis.</p>

    <p>Lorem ipsum dolor sit amet, officia excepteur ex fugiat reprehenderit enim labore culpa sint ad nisi Lorem pariatur mollit ex esse exercitation amet. Nisi anim cupidatat excepteur officia. Reprehenderit nostrud nostrud ipsum Lorem est aliquip amet voluptate voluptate dolor minim nulla est proident. Nostrud officia pariatur ut officia. Sit irure elit esse ea nulla sunt ex occaecat reprehenderit commodo officia dolor Lorem duis laboris cupidatat officia voluptate. Culpa proident adipisicing id nulla nisi laboris ex in Lorem sunt duis officia eiusmod. Aliqua reprehenderit commodo ex non excepteur duis sunt velit enim. Voluptate laboris sint cupidatat ullamco ut ea consectetur et est culpa et culpa duis.</p>
    
    <p>Lorem ipsum dolor sit amet, officia excepteur ex fugiat reprehenderit enim labore culpa sint ad nisi Lorem pariatur mollit ex esse exercitation amet. Nisi anim cupidatat excepteur officia. Reprehenderit nostrud nostrud ipsum Lorem est aliquip amet voluptate voluptate dolor minim nulla est proident. Nostrud officia pariatur ut officia. Sit irure elit esse ea nulla sunt ex occaecat reprehenderit commodo officia dolor Lorem duis laboris cupidatat officia voluptate. Culpa proident adipisicing id nulla nisi laboris ex in Lorem sunt duis officia eiusmod. Aliqua reprehenderit commodo ex non excepteur duis sunt velit enim. Voluptate laboris sint cupidatat ullamco ut ea consectetur et est culpa et culpa duis.</p>
  </div>
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
  grid-template-columns: 7fr 3fr;
}

.main > div {
  height: 100%;
}

.tutorial {
  overflow: auto;
}

.tutorial h2 {
  font-size: 1.4rem;
}

.tutorial p {
  padding: 1rem;
  font-size: 1rem;
}
</style>

