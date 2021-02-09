<template>
  <a-sub-menu key="menuRouters.name" v-if="testIt">
    <span slot="title"
      ><a-icon :type="menuRouters.meta.icon" /><span>{{
        menuRouters.meta.title
      }}</span></span
    >
    <a-menu-item
      v-for="item in menuRouters.children"
      :key="item.path"
      @click="jumpRouter(item.path)"
    >
      {{ item.meta.title }}
    </a-menu-item>
  </a-sub-menu>
</template>

<script>
export default {
  props: ["menuRouters"],
  data() {
    console.log(this.menuRouters);
    return {};
  },
  computed: {
    testIt() {
      if (this.menuRouters) {
        return true;
      } else {
        return false;
      }
    }
  },
  methods: {
    jumpRouter(willpush) {
      if (this.$route.path === willpush) {
        console.log("need not to jump");
      } else {
        this.$router.push({ path: willpush, query: this.$route.query });
      }
    }
  }
};
</script>

<style></style>
