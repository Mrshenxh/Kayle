<template>
  <a-menu theme="dark" :default-selected-keys="['1']" mode="inline">
    <sub-menu
      v-for="(item, index) in subMenuRoute"
      :key="index"
      :menuRouters="item"
    ></sub-menu>
  </a-menu>
</template>

<script>
import SubMenu from "@/components/layout/SubMenu";
import getAllSliderRouter from "@/utils/getrouter.js";

export default {
  data() {
    return {
      subMenuRoute: getAllSliderRouter(this)
    };
  },
  components: {
    SubMenu
  }
};
</script>

<style></style>
