<template>
  <div id='temp'>
      <Button type="info" @click="routerChange">跳转</Button>
      <Button v-if="$route.name==='login'" type="info" @click="login">登陆</Button>
      <Button v-else type="info" @click="logout">退出</Button>
      
      {{$route.name}}
  </div>
</template>

<script>
import pas from "../api/api";
export default {
  data() {
    return {
      number: 1,
      
    };
  },
  methods: {
    routerChange() {
      this.number++;
      if (this.number > 10) {
        this.number = 1;
      }
      this.$router.push({ name: "temp" + String(this.number) });
    },
    login() {
      this.$loginAjax(pas.login).then(res => {
        if (res.data.code === 200) {
          this.$store.commit("changeHcToken", res.data.data.hcip_token);
          this.$router.push({ name: "temp1" });
        }
      });
    },
    logout() {
      this.$loginAjax(pas.logout).then(res => {
        if (res.data.code === 200) {
          this.$router.push({ name: "login" });
        }
      });
    },
    
  }
};
</script>
