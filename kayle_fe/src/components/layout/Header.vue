<template>
  <div class="Headers">
    <label style="font-size: calc(12%)">
      <span>
        <h1 style="display:inline;">凯尔测试</h1>
      </span>
    </label>
    <a-dropdown class="components-dropdown-demo-placement">
      <label>
        <a-avatar :size="36" icon="user" />
        <span style="font-size: calc(8%);margin-left:calc(1%)">{{
          nickName
        }}</span>
      </label>
      <a-menu slot="overlay">
        <a-menu-item>
          <label>个人设置</label>
        </a-menu-item>
        <a-menu-item>
          <label>问题反馈</label>
        </a-menu-item>
        <a-menu-item>
          <label>关于我们</label>
        </a-menu-item>
        <!-- <a-menu-item style="height: 10px;">
                    <a-menu-divider></a-menu-divider>
                </a-menu-item> -->
        <a-menu-item>
          <label @click="clickLogout">退出登录</label>
        </a-menu-item>
      </a-menu>
    </a-dropdown>
  </div>
</template>

<script>
import request from "@/utils/request";
import { message } from "ant-design-vue";

export default {
  data() {
    return {
      nickName: undefined
    };
  },
  created() {
    request({
      url: "/api/user/message",
      method: "POST"
    }).then(res => {
      if (res.data.code === 120000) {
        this.nickName = res.data.data.nick_name;
      }
    });
  },
  methods: {
    clickLogout() {
      //点击退出登录，将相关数据置为空
      request({
        url: "/api/user/logout",
        method: "POST"
      }).then(res => {
        if (res.data.code === 100003) {
          this.nickName = undefined;
          this.$store.commit("removeUserMessage");
          this.$router.push("/user/login");
          message.success("退出登录成功");
        } else {
          message.error(res.data.msg);
        }
      });
    }
  }
};
</script>

<style scoped>
.Headers {
  display: inline;
  text-align: center;
  margin-left: calc(50% - 100px);
}

.components-dropdown-demo-placement {
  margin-right: 8px;
  margin-bottom: 8px;
  width: calc(15%);
  margin-left: calc(40% - 80px);
}
</style>
