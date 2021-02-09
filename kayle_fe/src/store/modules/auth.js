import router from "../../router";
import request from "@/utils/request";
import { notification } from "ant-design-vue";

const auth = {
  state: () =>
    JSON.parse(sessionStorage.getItem("auth")) || {
      userId: "test",
      userName: "",
      nickName: "",
      userIcon: "",
      userMessage: ""
    },

  mutations: {
    saveUserMessage(state, payload) {
      sessionStorage.setItem("auth", JSON.stringify(payload));
      state.userId = payload.user_id;
      state.userName = payload.username;
      state.nickName = payload.nick_name;
      state.userIcon = payload.user_icon;
      state.userMessage = payload.user_message;
      router.push(payload.toRoute);
    },
    // 退出登录时清除用户信息
    removeUserMessage() {
      sessionStorage.removeItem("auth");
    }
  },

  actions: {
    async justLoginSystem({ commit }, { payload }) {
      await request({
        url: "/api/user/login",
        method: "POST",
        data: payload
      }).then(res => {
        if (res.data.code === 100000) {
          request({
            url: "/api/user/message",
            method: "POST"
          }).then(ress => {
            if (ress.data.code === 120000) {
              commit("saveUserMessage", { ...ress.data.data, toRoute: "/" });
            }
          });
        } else {
          notification.error({
            //eslint-disable-next-line no-unused-vars
            message: h => (
              <div>
                登录错误: <span style="color: red">{res.data.msg}</span>
              </div>
            ),
            description: "请正确填写您的账号密码，如果遗忘请及时更换密码！"
          });
        }
      });
    }
  }
};

export default auth;
