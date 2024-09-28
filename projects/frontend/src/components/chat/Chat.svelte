<script>
let { messages } = $props();

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
    <input type="text">
    <button>send</button>
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
}

.message {
  margin: 2rem 1rem;
  max-width: 75%;
}

.message-user {
  margin-left: auto;
}

.message-server {
  margin-right: auto;
}
</style>
