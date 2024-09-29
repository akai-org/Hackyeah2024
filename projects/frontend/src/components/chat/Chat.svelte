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
let taxFill = $state(false);
// `on` should show the ui for confirming
// `send` should send next WS packet as correction
let toCorrect = $state({ on: false, send: false, correction_id: "" });

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

  if (msg.correction_id !== undefined) {
    toCorrect = { on: true, send: true, correction_id: msg.correction_id };
  }

  // Check if we should suggest a help with PCC tax shit
  if (taxFill !== true) {
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

  if (toCorrect.send == true) {
    wsSend.set({ correction: input, correction_id: toCorrect.correction_id });
    messages.push({
      id: -1,
      time: Date.now(),
      owner: "user",
      text: input,
    });


    return;
  }

  wsSend.set({ message: input });
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

  fetch('http://192.168.13.68:8000/api/audio/', {
    method: 'POST',
    body: formData,
    class: "chat",
    headers: {
      "Authorization": `Bearer ${window.X_HIDDEN.access}`,
    },
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
        text: data.transcription,
      });
      wsSend.set({ message: data.transcription });

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
    owner: "server",
    class: "message"
  });
  isDisabled = true;
}

function sendFile(e) {
  e.preventDefault();


  const fileInput = document.getElementById("special_file");
  const file = fileInput.files[0];

  if (file !== undefined) {
    const formData = new FormData();
    formData.append("photo.jpg", file);

    // TODO: IP
    fetch("http://192.168.13.68:8000/api/photo/", {
      method: 'POST',
      body: formData,
      headers: {
        "Authorization": `Bearer ${window.X_HIDDEN.access}`,
      },
    })
      .then(data => data.json())
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

function handleSpecialCase() {
  taxFill = true;

  wsSend.set({ mode: "PCC-3" });
  awaitResponse();
}

function handleCorrection(is_correct) {
  isDisabled = true;

  wsSend.set({ is_correct, correction_id: toCorrect.correction_id });
  awaitResponse();

  toCorrect.on = false;

  if (is_correct === false) {
    input = messages.at(-1).text;
  }
}
</script>

<div class="chat">
  <div class="title">
    <h1><i class="bi bi-file-earmark-check-fill fa-3x"></i>Your awesome assistant</h1>
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
    <input class="form-control" id="input-text" placeholder="O co chcesz sie zapytać" onkeypresscapture={keyEnter} type="text" bind:value={input} disabled={isDisabled}>
    <button type="button" class="btn btn-secondary" onclick={send} disabled={isDisabled}><i class="bi bi-chat-right-text"></i> send</button>
    <button type="button" class="btn btn-dark" onclick={audio} disabled={isDisabled}><i class="bi bi-mic"></i> {isAudioRunning ? "STOP AUDIO" : "GO AUDIO"}</button>

    <form onsubmit={sendFile} class="{taxFill ? '' : 'hidden'}">
      <input  type="file" id="special_file" disabled={isDisabled}>
      <input type="submit" value="Send file" disabled={isDisabled}>
    </form>

    {#if taxFill === false} 
      <button class="{specialCase ? '' : 'hidden'} btn btn-info" onclick={handleSpecialCase}>
        Czy checesz pomocy w wypełnienieniu deklaracji PPC-3?  
      </button>
    {:else if toCorrect.on === true}
      <div>
        <button class="btn btn-success" onclick={() => handleCorrection(true)}>Data is correct</button>
        <button class="btn btn-warning" onclick={() => handleCorrection(false)}>Data is not correct</button>
      </div>
    {/if}
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

