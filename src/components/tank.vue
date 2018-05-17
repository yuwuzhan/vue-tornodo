<template>
  <div id="tank">
      <div class="wid1200">
      <div class="tank-temp">
        <canvas id="tutor" width="800" height="800" style="position:absolute">
        </canvas>
        <canvas id="bullet" width="800" height="800">
        </canvas>
      </div>
      <Button class="leftBut" @click="joinTank">加入</Button>
      </div>
      <div style="width:600px;height:600px">
        <div style="border:1px solid #ddd;width:100%;padding-bottom:56.25%"></div>
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
      bulletCanvas: "",
      bulletCtx: "",
      timer: null,
      bulletList: [],
      initColor: {
        0: "rgba(0, 0, 200, 0.5)",
        1: "rgba(0, 200, 0, 0.5)",
        2: "rgba(200, 0, 0, 0.5)",
        3: "rgba(200, 200, 200, 0.5)"
      },
      player: [],
      keydowns: {
        87: 0,
        83: 0,
        65: 0,
        68: 0
      },
      keyaction: {
        87: [0, -1],
        83: [0, 1],
        65: [-1, 0],
        68: [1, 0]
      },
      initDirection: {
        0: [0, -1],
        1: [1, 0],
        2: [0, 1],
        3: [-1, 0]
      },
      direction: []
    };
  },
  methods: {
    joinTank() {
      if (!this.ws || this.ws.readyState === 3) {
        this.ws = new WebSocket(baseUrls.tank);
        this.ws.onopen = () => {
          console.log("send");
          window.addEventListener("keydown", this.keydownEvt);
          window.addEventListener("keyup", this.keyupEvt);
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
            case 99:
              this.addBullet(data.mes);
              break;
            default:
              console.log(data.mes);
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
      if (mes.id !== undefined) {
        this.direction = this.initDirection[mes.id];
      }
      mes.numbers &&
        mes.numbers.forEach(element => {
          this.ctx.fillStyle = this.initColor[element.id];
          this.ctx.fillRect(
            element.pos.x,
            element.pos.y,
            element.pos.size,
            element.pos.size
          );
          this.ctx.font = "16px serif";
          this.ctx.strokeText(element.name, element.pos.x, element.pos.y + 22);
        });
      // mes.bullets.forEach(element => {
      //   this.ctx.fillStyle = this.initColor[element.id];
      //   this.ctx.fillRect(element.x, element.y, element.size, element.size);
      // });
    },

    keydownEvt(e) {
      // console.log(e);
      if (
        e.keyCode === 87 ||
        e.keyCode === 83 ||
        e.keyCode === 65 ||
        e.keyCode === 68
      ) {
        this.keyaction[e.keyCode].forEach((v, index) => {
          if (v) {
            this.direction[index] = v;
          }
        });
        this.keydowns[e.keyCode] = 1;
        this.ws.send(
          JSON.stringify({ key: this.keydowns, direction: this.direction })
        );
      }
      if (e.keyCode === 32) {
        this.ws.send(JSON.stringify({ key: e.keyCode }));
        // this.renderBullet();
      }
      e.preventDefault();
    },
    addBullet(msg) {
      console.log(msg.bullets);
      this.bulletList.push(msg.bullets);
      clearInterval(this.timer);
      this.timer = setInterval(_ => {
        this.bulletList.forEach((v, index, arr) => {
          arr[index].y += v.direction[1] * v.speed;
          arr[index].x += v.direction[0] * v.speed;
          if (v.y > 800 || v.y < 0 || v.x > 800 || v.x < 0) {
            arr.slice(index, 1);
          }
          this.bulletCtx.clearRect(
            v.x - v.direction[0] * v.speed,
            v.y - v.direction[1] * v.speed,
            10,
            10
          );
          this.bulletCtx.fillRect(v.x, v.y, 10, 10);
        });
      }, 1000 / 60);
    },
    // renderBullet() {
    //   // clearInterval(this.timerList)
    //   this.x = 0;
    //   this.y = 760;
    //   this.bulletCtx.fillStyle = this.initColor[0];
    //   this.bulletList.push(this.y);
    //   // console.log(this.bulletList);
    //   clearInterval(this.timer);
    //   this.timer = setInterval(_ => {
    //     this.bulletList.forEach((v, index, arr) => {
    //       arr[index] -= 10;
    //       this.bulletCtx.clearRect(0, v + 10, 10, 10);
    //       this.bulletCtx.fillRect(0, v, 10, 10);
    //     });
    //   }, 1000 / 60);
    // },
    keyupEvt(e) {
      console.log(e);
      if (
        e.keyCode === 87 ||
        e.keyCode === 83 ||
        e.keyCode === 65 ||
        e.keyCode === 68
      ) {
        this.keydowns[e.keyCode] = 0;
        this.ws.send(
          JSON.stringify({ key: this.keydowns, direction: this.direction })
        );
      }
      e.preventDefault();
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
    this.bulletCanvas = document.getElementById("bullet");
    this.ctx = this.canvas.getContext("2d");
    this.bulletCtx = this.canvas.getContext("2d");
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
