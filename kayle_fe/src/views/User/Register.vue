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
        placeholder="请输入注册账号"
        allow-clear
      >
        <a-icon slot="prefix" type="user" style="color:rgba(0,0,0,.25)" />
      </a-input>
    </a-form-model-item>

    <a-form-model-item>
      <a-input
        v-model="formInline.nickname"
        placeholder="请输入注册用户姓名"
        allow-clear
      >
        <a-icon slot="prefix" type="user" style="color:rgba(0,0,0,.25)" />
      </a-input>
    </a-form-model-item>

    <a-form-model-item>
      <a-input-password
        v-model="formInline.password"
        type="password"
        placeholder="请输入注册密码"
      >
        <a-icon slot="prefix" type="lock" style="color:rgba(0,0,0,.25)" />
      </a-input-password>
    </a-form-model-item>

    <a-form-model-item>
      <a-input-password
        v-model="formInline.confirm"
        type="password"
        placeholder="请确认注册密码"
      >
        <a-icon slot="prefix" type="lock" style="color:rgba(0,0,0,.25)" />
      </a-input-password>
    </a-form-model-item>

    <a-form-model-item>
      <a-button
        class="loginButton"
        type="primary"
        html-type="submit"
        :disabled="
          formInline.username === '' ||
            formInline.password === '' ||
            formInline.confirm === '' ||
            formInline.nickname === ''
        "
      >
        注册
      </a-button>
    </a-form-model-item>
  </a-form-model>
</template>

<script>
import request from "@/utils/request";
import { message } from "ant-design-vue";

export default {
  data() {
    return {
      formInline: {
        username: "",
        password: "",
        confirm: "",
        nickname: ""
      }
    };
  },
  methods: {
    handleSubmit(e) {
      console.log(e);
      console.log({ ...this.formInline });
      request({
        url: "/api/user/register",
        method: "POST",
        data: this.formInline
      }).then(res => {
        if (res.data.code === 110000) {
          request({
            url: "/api/user/message",
            method: "POST"
          }).then(ress => {
            if (ress.data.code === 120000) {
              this.$store.commit("saveUserMessage", {
                ...ress.data.data,
                toRoute: "/"
              });
            }
          });
        } else {
          message.warning(res.data.msg);
        }
      });
    },
    onChange(e) {
      console.log(`checked = ${e.target.checked}`);
    },
    jumpRegister() {
      this.$router.push("/user/register");
    }
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
