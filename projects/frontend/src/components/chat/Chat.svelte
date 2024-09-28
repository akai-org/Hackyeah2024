<script>
import { messageStore, wsSend } from "../../libs/webSocket.js";
import { onMount } from "svelte";

let messages = $state([]);
let input = $state("");
let isDisabled = $state(false);
let isAudioRunning = $state(false);
// Special here means case when we detect that message contains `PCC` word therefore ask the user
// if they want help with it??
let specialCase = $state(true);

onMount(() => {
});

messageStore.subscribe(msg => {
  if (!msg.message) {
    return;
  }

  // "should" always evaluate to `true` -- sanity check
  if (messages.at(-1).awaiting) {
    messages.pop();
  }

  // Check if we should suggest a help with PCC tax shit
  {
    let m = msg.message;

    if (
      m.indexOf("PCC-3") !== -1
      || m.indexOf("PCC3") !== -1
      // TODO: Maybe `PCC` as well
    ) {
      specialCase = true;
    }
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
  if (input === "") {
    // NOPE
    return;
  }
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
    awaitResponse();

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

  // TODO: IP
  fetch('/api/upload-voice', {
    method: 'POST',
    body: formData,
  })
    .then(response => {
      console.log("AUDIO RESPONSE:", response);
      return response.json();
    })
    .then(data => {
      messages.push({
        id: -1,
        time: Date.now(),
        owner: "user",
        text: data.message,
      });
      wsSend.set(JSON.stringify({ message: data.message }));

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
  isDisabled = true;
}

function sendFile(e) {
  e.preventDefault();


  const fileInput = document.getElementById("special_file");
  const file = fileInput.files[0];

  if (file !== undefined) {
    const formData = new FormData();
    formData.append(file.name, file);

    // TODO: IP
    fetch('/upload-file', {
      method: 'POST',
      body: formData,
    })
      .then(data => {
        console.log('File uploaded successfully:', data);

        messages.push({
          text: file.name,
          owner: "user",
          isFile: true,
        });
        awaitResponse();
      })
      .catch(error => {
        console.error('Error uploading file:', error);
      });
  } else {
    alert('Please select a file to upload.');
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
        class="message message--{message.owner} {message.isFile && 'message--file'}"
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

    <form onsubmit={sendFile}>
      <input class="{specialCase ? '' : 'hidden'}" type="file" id="special_file" disabled={isDisabled}>
      <input type="submit" value="Send file" disabled={isDisabled}>
    </form>

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

.message--user {
  margin-left: auto;
  text-align: right;
}

.message--server {
  margin-right: auto;
}

.message--file {
  background-color: purple;
}

.hidden {
  visibility: hidden;
}
</style>

