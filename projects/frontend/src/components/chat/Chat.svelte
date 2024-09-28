<script>
import { messageStore, wsSend } from "../../libs/webSocket.js";
import { onMount } from "svelte";

let messages = $state([]);
let input = $state("");
let isDisabled = $state(false);

onMount(() => {
});

messageStore.subscribe(msg => {
  // WTF??
  console.log("SUBSCRIE", msg, messages);
  if (!msg.message) {
    return;
  }

  messages.push({
    text: msg.message,
    time: new Date(msg.time),
    owner: "server",
    id: msg.id,
  });

  isDisabled = false;
});

function send() {
  wsSend.set(JSON.stringify({ message: input }));
  messages.push({
    id: -1,
    time: Date.now(),
    owner: "user",
    text: input,
  });

  input = "";
  isDisabled = true;
}

function keyEnter(e) {
  // 13 is `Enter` key
  if (e.keyCode === 13) {
    send();
  }
}
</script>

<div class="chat">
  <div class="title">
    <h1>Your awesome assistant</h1>
  </div>
  <div class="body">
    {#each messages as message}
      <div
        class="message message-{message.owner}"
      >
        <span>
          {message.text}
        </span>
      </div>
    {/each}
  </div>
  <div class="input">
    <input onkeypresscapture={keyEnter} type="text" bind:value={input} disabled={isDisabled}>
    <button onclick={send} disabled={isDisabled}>send</button>
  </div>
</div>

<style>
.chat {
  height: 100%;
  padding: 1rem;
}

.title {
  font-size: 1rem;
}

.body {
  padding: 1rem 0.5rem;
  display: flex;
  flex-direction: column;
  min-height: 50%;
}

.message {
  margin: 2rem 1rem;
  padding: 1rem;
  max-width: 75%;
}

.message-user {
  margin-left: auto;
  text-align: right;
}

.message-server {
  margin-right: auto;
}
</style>

