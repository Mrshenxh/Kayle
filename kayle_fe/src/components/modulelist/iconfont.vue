<template>
  <icon-font :type="iconType" />
</template>
<script>
import { Icon } from "ant-design-vue";

const IconFont = Icon.createFromIconfontCN({
  scriptUrl: "//at.alicdn.com/t/font_2176213_dmsf985jxuf.js"
});
export default {
  props: ["iconType"],
  components: {
    IconFont
  }
};
</script>
<style scoped></style>
