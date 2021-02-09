<template>
  <a-form-model
    class="formModule"
    layout="horizontal"
    :model="formInline"
    @submit="handleSubmit"
    @submit.native.prevent
  >
    <a-form-model-item>
      <a-input
        v-model="formInline.username"
        placeholder="请输入平台账号"
        allow-clear
      >
        <a-icon slot="prefix" type="user" style="color:rgba(0,0,0,.25)" />
      </a-input>
    </a-form-model-item>
    <a-form-model-item>
      <a-input-password
        v-model="formInline.password"
        type="password"
        placeholder="请输入平台密码"
      >
        <a-icon slot="prefix" type="lock" style="color:rgba(0,0,0,.25)" />
      </a-input-password>
      <div style="justify-content: space-between;display: flex;">
        <a-checkbox
          v-model="formInline.checked"
          @change="onChange"
          style="user-select:none;"
          >自动登录</a-checkbox
        >
        <label class="lostPassward">忘记密码?&nbsp;</label>
      </div>
    </a-form-model-item>
    <a-form-model-item>
      <a-button
        class="loginButton"
        type="primary"
        html-type="submit"
        :disabled="formInline.user === '' || formInline.password === ''"
      >
        登录
      </a-button>
    </a-form-model-item>
    <a-form-item>
      <div style="justify-content: space-between;display: flex;">
        <span
          ><iconfont
            style="font-size:20px"
            iconType="icon-icon_huabanfuben"
          ></iconfont
          >&nbsp;关于凯尔</span
        >
        <a-button type="primary" @click="jumpRegister">注册账户</a-button>
      </div>
    </a-form-item>
  </a-form-model>
</template>
<script>
import iconfont from "@/components/modulelist/iconfont";

export default {
  data() {
    return {
      formInline: {
        username: "",
        password: "",
        checked: false
      }
    };
  },
  methods: {
    handleSubmit(e) {
      console.log(e);
      console.log({ ...this.formInline });
      this.$store.dispatch({
        type: "justLoginSystem",
        payload: { ...this.formInline }
      });
    },
    onChange(e) {
      console.log(`checked = ${e.target.checked}`);
    },
    jumpRegister() {
      this.$router.push("/user/register");
    }
  },
  components: {
    iconfont
  }
};
</script>
<style scoped>
@media (min-width: 900px) {
  .formModule {
    width: calc(25%);
    margin-left: calc(37.5%);
    margin-top: 40px;
  }
}

@media (max-width: 900px) {
  .formModule {
    width: calc(45%);
    margin-left: calc(28.5%);
    margin-top: 20px;
  }
}

.loginButton {
  width: calc(100%);
  height: 40px;
}

.lostPassward {
  /* margin-right:-10px; */
  user-select: none;
}

.lostPassward:hover {
  cursor: pointer;
  color: brown;
  /*光标呈现为指示链接的指针（一只手）*/
}
</style>
