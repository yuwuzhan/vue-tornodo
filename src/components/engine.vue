<template>
  <div id="engine">
    <div style="width:50%;height:50%">
      <div class="wrapper">
        <div class="item item1">head</div>
        <div class="item item2">menu</div>
        <div class="item item3">
          <canvas id="canvas"></canvas>
          <div style="height:1600px"></div>
        </div>
        <div class="item item4">footer</div>
      </div>
    </div>
    <div style="width:50%">

    </div>
  </div>
</template>
<script>
import Matter from 'matter-js'
export default {
  data() {
    return {}
  },
  mounted() {
    var img = new Image()

    // User Variables - customize these to change the image being scrolled, its
    // direction, and the speed.

    img.src =
      'https://mdn.mozillademos.org/files/4553/Capitan_Meadows,_Yosemite_National_Park.jpg'
    var CanvasXSize = 800
    var CanvasYSize = 200
    var speed = 30 //lower is faster
    var scale = 1.05
    var y = -4.5 //vertical offset

    // Main program

    var dx = 0.75
    var imgW
    var imgH
    var x = 0
    var clearX
    var clearY
    var ctx

    img.onload = function() {
      imgW = img.width * scale
      imgH = img.height * scale
      if (imgW > CanvasXSize) {
        x = CanvasXSize - imgW
      } // image larger than canvas
      if (imgW > CanvasXSize) {
        clearX = imgW
      } else {
        // image larger than canvas
        clearX = CanvasXSize
      }
      if (imgH > CanvasYSize) {
        clearY = imgH
      } else {
        // image larger than canvas
        clearY = CanvasYSize
      }
      //Get Canvas Element
      ctx = document.getElementById('canvas').getContext('2d')
      //Set Refresh Rate
      return setInterval(draw, speed)
    }

    function draw() {
      //Clear Canvas
      ctx.clearRect(0, 0, clearX, clearY)
      //If image is <= Canvas Size
      if (imgW <= CanvasXSize) {
        //reset, start from beginning
        if (x > CanvasXSize) {
          x = 0
        }
        //draw aditional image
        if (x > CanvasXSize - imgW) {
          ctx.drawImage(img, x - CanvasXSize + 1, y, imgW, imgH)
        }
      } else {
        //If image is > Canvas Size
        //reset, start from beginning
        if (x > CanvasXSize) {
          x = CanvasXSize - imgW
        }
        //draw aditional image
        if (x > CanvasXSize - imgW) {
          ctx.drawImage(img, x - imgW + 1, y, imgW, imgH)
        }
      }
      //draw image
      ctx.drawImage(img, x, y, imgW, imgH)
      //amount to move
      x += dx
    }
    // // module aliases
    // var Engine = Matter.Engine,
    //   Render = Matter.Render,
    //   World = Matter.World,
    //   Bodies = Matter.Bodies;

    // // create an engine
    // var engine = Engine.create();

    // // create a renderer
    // var render = Render.create({
    //   element: document.getElementById("qqq"),
    //   engine: engine
    // });

    // // create two boxes and a ground
    // var boxA = Bodies.rectangle(400, 200, 80, 80);
    // var boxB = Bodies.rectangle(450, 50, 80, 80);
    // var ground = Bodies.rectangle(400, 610, 810, 60, { isStatic: true });

    // // add all of the bodies to the world
    // World.add(engine.world, [boxA, boxB, ground]);

    // // run the engine
    // Engine.run(engine);

    // // run the renderer
    // Render.run(render);
  },
  methods: {}
}
</script>
<style>
.engine-body {
  width: 1200px;
  margin: 0 auto;
}
.wrapper {
  height: 100%;
  display: grid;
  /* grid-gap: 1px; */
  grid-template-columns: repeat(12, 1fr);
  grid-template-rows: 10% 80% 10%;
  grid-template-areas:
    'h h h h h h h h h h h h'
    'm m c c c c c c c c c c'
    'm m f f f f f f f f f f';
}
@media screen and (max-width: 768px) {
  .wrapper {
    grid-template-rows: 10% 10% 70% 10%;
    grid-template-areas:
      'h h h h h h h h h h h h'
      'm m m m m m m m m m m m'
      'c c c c c c c c c c c c'
      'f f f f f f f f f f f f';
  }
  .item2 {
    border-right: none;
    border-bottom: 1px solid #fff;
  }
}
.item {
  box-sizing: border-box;
  border-radius: 8px;
}
.item1 {
  border-bottom: 1px solid #fff;
  grid-area: h;
  background-color: aqua;
}
.item2 {
  border-right: 1px solid #fff;
  grid-area: m;
  background-color: aquamarine;
}
.item3 {
  overflow-y: auto;
  border-bottom: 1px solid #fff;
  grid-area: c;
  background-color: beige;
}
.item4 {
  grid-area: f;
  background-color: rebeccapurple;
}
</style>


