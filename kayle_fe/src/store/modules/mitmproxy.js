import request from "@/utils/request";
import { notification } from "ant-design-vue";

const mitmproxy = {
  state: () =>
    JSON.parse(sessionStorage.getItem("mitmproxy")) || {
      port: "",
      host_list: "",
      mitm_id: "",
      expire_time: ""
    },

  mutations: {
    saveUserMitmproxy(state, payload) {
      sessionStorage.setItem("mitmproxy", JSON.stringify(payload));
      state.port = payload.port;
      (state.host_list = payload.host_list),
        (state.mitm_id = payload.mitm_id),
        (state.expire_time = payload.expire_time);
    },
    // 清除用户mitmproxy
    removeUserMitmproxy() {
      sessionStorage.removeItem("mitmproxy");
    }
  },

  actions: {
    async getUserMitmproxy({ commit }) {
      await request({
        url: "/api/tempinter/queryusersocket",
        method: "POST"
      }).then(res => {
        if (res.data.code === 230000) {
          // 该用户有对应端口号 操作初始化
          commit("saveUserMitmproxy", { ...res.data.data });
          return 230000;
        } else if (res.data.code === 230002) {
          // 没有对应端口号 展示对应创建组件
          console.log("展示对应创建组件");
          return 230002;
        } else {
          notification.error({
            //eslint-disable-next-line no-unused-vars
            message: h => (
              <div>
                查询错误: <span style="color: red">{res.data.msg}</span>
              </div>
            ),
            description: "请使用正确的请求方式！"
          });
          return -1;
        }
      });
    },
    deleteUserMitmproxy({ commit }) {
      commit("removeUserMitmproxy");
    }
  }
};

export default mitmproxy;
