import { writable } from "svelte/store";

export const messageStore = writable({});
export const wsSend = writable();

const loc = window.location;
const wsProtocol = loc.protocol === "https:" ? "wss://" : "ws://";
// 8443
const ws = new WebSocket(`ws://192.168.13.68:8001/ws/chat/`);

wsSend.subscribe(data => {
  if (data === undefined) return;
  try {
    const parse = JSON.stringify(data);

    //console.log(parse);
    ws.send(parse);
  } catch (err) {
    console.error("Failed to parse message that was to be send to WS", err);
  }
});

ws.onopen = () => {
  console.log("WS Connection open");

  messageStore.set({connected: true});
}

ws.onopen = () => {
  console.log("WS Connection open");

  messageStore.set({connected: true});
}

ws.onmessage = message => {
  let data;
  try {
    data = JSON.parse(message.data);

    console.log("WS DATA:", data);
  } catch (err) {
    console.error("cant parse WS message", err);

    // TODO: We we are still connected it's just to mimic an error
    messageStore.set({connected: false});

    return;
  }

  messageStore.set(data);
}

ws.onerror = error => {
  console.error("WS ERROR", error);

  messageStore.set({connected: false});
}

ws.onclose = () => {
  messageStore.set({connected: false});

  console.log("WS CLOSED");
}
