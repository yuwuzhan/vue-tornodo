<template>
  <div id='game'>
      <Button @click="sendmsg">发送消息</Button>
      <Input v-model="msg" type="textarea" :rows="4" placeholder="说点啥。。。"></Input>
      <div v-for="each in rece">
        {{each}}
      </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      ws: "",
      msg: "",
      rece: [],
    };
  },
  methods: {
    sendmsg() {
      this.ws.send(this.msg);
    }
  },
  mounted() {
    if (!this.ws||this.ws.readyState===3) {
      this.ws = new WebSocket("ws://192.168.1.70:8124/ws");
      this.ws.onopen = () => {
      };
      this.ws.onmessage = evt => {
        console.log("get message", evt.data);
        this.rece.push(evt.data);
        if (this.rece.length > 50) {
          this.rece.shift();
        }
      };
      this.ws.onclose = evt => {
        console.log("wsclose", evt);
      };
      this.ws.onerror = evt => {
        console.log("error");
      };
    }
  }
};
</script>

