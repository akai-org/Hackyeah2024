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

    <p>Witamy na stronie eRachmistrz.egzaminword.pl gdzie asystent podatkowy wykorzystujący sztuczną inteligencję ma za zadanie pomóc ci wypełnić zeznanie podatkowe</p>

    <p>Po lewej stronie można zobaczyć okno służące do interakcji z użytkownikiem, tam asystent pyta i odpowiada użytkownikom w formie wizualnej.</p>
    
    <p>Nie jest to jednak jedyna możliwość. eRachmistrz obsługuje odpowiedzi głosowe! Zadaj pytanie, a chatbot odpowie głosem, dzięki czemu możesz słuchać odpowiedzi zamiast czytać.</p>
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

.tutorial h1 {
  font-size: 1.4rem;
}

.tutorial p {
  padding: 1rem;
  font-size: 1rem;
}
</style>
