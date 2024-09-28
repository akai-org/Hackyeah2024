<script>
let { page = $bindable() } = $props();

let error = $state(false);
let username = $state("");
let password = $state("");

async function login(e) {
  e.preventDefault();

  console.log("PASS:", username, password);
  try {
    console.log("herhe");
    const response = await fetch(
      "http://192.168.13.68:8000/api/token/",
      {
        method: "POST",
        body: JSON.stringify({
          username,
          password,
        }),
      }
    );

    console.log("adf", response);


    if (response.ok === false) {
      error = true;

      return;
    }


    const json = await response.json();

    console.log("API RETURN:", json);


    // I HATE THIS I HATE THIS I HATE THIS
    // BACKEND HAS FORCED MY HAND
    window.X_HIDDEN = {};
    window.X_HIDDEN.refresh = json.refresh;
    window.X_HIDDEN.access = json.access;

    page = 1;
  } catch (err) {
    console.error(err);

    error = true;
  }
}
</script>


<div class="main">
  <form class="inner">
    <h1>Login</h1>

    <label for="username">Username</label>
    <input type="text" id="username" bind:value={username}>

    <label for="password">Password</label>
    <input type="password" id="password" bind:value={password}>

    <span class="{error === true ? 'show_error' : ''}">Wrong username or password</span>
    <input type="button" value="Submit" onclick={login}>
  </form>
</div>

<style>
.main {
  display: flex;
  flex-direction: column;
  height: 100%;
}

form {
  border: 0.1rem solid #000;
  margin: auto;
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

h1 {
  margin: auto;
}

label {
  margin-bottom: 0.5rem;
  margin-top: 2rem;
}

input {
  padding: 0.5rem;
  font-size: 2rem;
}

input[type = "button"] {
  margin-top: 2rem;
}

/* This is shown when login fails */
span {
  margin: 1rem auto 0 auto;
  color: #f00;
  visibility: hidden;
}

.show_error {
  visibility: visible;
}
</style>

