<template>
  <div id="tank">
      <div class="wid1200">
      <div class="tank-temp">
        <canvas id="tutor" width="800" height="800">

        </canvas>
      </div>
      <Button class="leftBut" @click="joinTank">加入</Button>
      </div>
      
  </div>
</template>
<script>
export default {
  data() {
    return {
      canvas: "",
      ctx: "",
      initColor: {
        0: "rgba(0, 0, 200, 0.5)",
        1: "rgba(0, 200, 0, 0.5)",
        2: "rgba(200, 0, 0, 0.5)",
        3: "rgba(200, 200, 200, 0.5)"
      },
      player: []
    };
  },
  methods: {
    joinTank() {
      if (!this.ws || this.ws.readyState === 3) {
        this.ws = new WebSocket("ws://192.168.1.70:8124/tank");
        this.ws.onopen = () => {
          console.log("send");
        };
        this.ws.onmessage = evt => {
          let data = JSON.parse(evt.data);
          console.log(data.type);
          switch (data.type) {
            case 0:
              this.clearPlayer(data.mes);
              break;
            case 2:
              this.initPosition(data.mes);
              break;
            case 3:
              this.changePosition(data.mes);
              break;
            case 4:
              this.infoGame(data.mes);
              break;
          }
        };
        this.ws.onclose = evt => {
          console.log("wsclose", evt);
        };
        this.ws.onerror = evt => {
          console.log("error");
        };
      }
    },
    initPosition(mes) {
      console.log(mes);
      mes.numbers.forEach(element => {
        if (!this.player.find(e => e.id === element.id)) {
          this.player.push(element);
          this.ctx.fillStyle = this.initColor[element.id];
          this.ctx.fillRect(
            element.pos.x,
            element.pos.y,
            element.pos.size,
            element.pos.size
          );
          this.ctx.strokeText(element.name, element.pos.x, element.pos.y);
        }
      });
    },
    changePosition(mes) {
      console.log(mes);
    },
    infoGame(mes) {
      alert(mes.info);
    },
    clearPlayer(res) {
      console.log(res);
    }
  },
  mounted() {
    this.canvas = document.getElementById("tutor");
    this.ctx = this.canvas.getContext("2d");
  }
};
</script>

<style scope>
.tank-temp {
  width: 800px;
  height: 800px;
  margin: 0 auto;
  border: 1px solid #ddd;
}
.leftBut {
  float: left;
  top: 50%;
  margin-top: -600px;
  margin-left: 120px;
}
.wid1200 {
  width: 1200px;
  margin: 0 auto;
}
</style>
