<script>
import { messageStore, wsSend } from "../../libs/webSocket.js";
import { onMount } from "svelte";

let messages = $state([]);
let input = $state("");
let isDisabled = $state(false);
let isAudioRunning = $state(false);

onMount(() => {
});

messageStore.subscribe(msg => {
  if (!msg.message) {
    return;
  }

  if (messages.at(-1).awaiting) {
    messages.pop();
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
  awaitResponse();

  input = "";
  isDisabled = true;
}

function keyEnter(e) {
  // 13 is `Enter` key
  if (e.keyCode === 13) {
    send();
  }
}

let mediaRecorder;

function audio() {
  if (isAudioRunning === true) {
    stopRecording();
    isAudioRunning = false;
    disabled = true;

    return;
  }

  let audioChunks = [];

  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
      isAudioRunning = true;
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        sendVoiceToBackend(audioBlob);
      };

      mediaRecorder.start();
    });
}

function stopRecording() {
  mediaRecorder.stop();
}

function sendVoiceToBackend(audioBlob) {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'voice.wav');

  // PCC3 PCC-3 ?PCC
  fetch('/api/upload-voice', {
    method: 'POST',
    body: formData,
  })
    .then(response => {
      console.log("AUDIO RESPONSE:", response);
      return response.json();
    })
    .then(data => {
      wsSend.set(JSON.stringify({ message: data.message }));
      messages.push({
        id: -1,
        time: Date.now(),
        owner: "user",
        text: input,
      });
      awaitResponse();

      console.log('Voice sent successfully:', data);
    })
    .catch(error => {
      console.error('Error sending voice:', error);
    });
}

function awaitResponse() {
  messages.push({
    awaiting: true,
    text: "Awating...",
  });
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
    <button onclick={audio} disabled={isDisabled}>{isAudioRunning ? "STOP AUDIO" : "GO AUDIO"}</button>
    <button class="hidden">Czy checesz pomocy w wypełnienieniu deklaracji PPC-3?</button>
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

