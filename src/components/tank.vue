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
import baseUrls from "../api/baseUrl";
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
        this.ws = new WebSocket(baseUrls.tank);
        this.ws.onopen = () => {
          console.log("send");
        };
        this.ws.onmessage = evt => {
          let data = JSON.parse(evt.data);
          switch (data.type) {
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
      this.ctx.clearRect(0, 0, 800, 800);
      console.log(mes);
      mes.numbers.forEach(element => {
        this.ctx.fillStyle = this.initColor[element.id];
        this.ctx.fillRect(
          element.pos.x,
          element.pos.y,
          element.pos.size,
          element.pos.size
        );
        this.ctx.font = "16px serif";
        this.ctx.strokeText(element.name, element.pos.x, element.pos.y+22);
      });
    },
    changePosition(mes) {
      console.log(mes);
    },
    infoGame(mes) {
      alert(mes.info);
    }
    // clearPlayer(res) {
    //   let outPlayer = this.player.find(r => r.id === res.id);
    //   this.player.splice(this.player.indexOf(outPlayer), 1);
    // }
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
