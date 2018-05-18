<template>
  <div id="app">
    <router-view class="app-items"></router-view>
  </div>
</template>

<script>
export default {
  data() {
    return {
      number: 0,
      join: false,
      name: null,
      users: null,
      message: null,
      messages: {}
    };
  },
  methods: {},
  sockets: {}
};
</script>

<style>
@import url('./static/css/main.css');
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height:100%;
  /* margin-top: 60px; */
}

html,
body {
  height: 100%;
}
.app-items{
  height: 100%;
}
body {
  margin: 0;
}
h1,
h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
