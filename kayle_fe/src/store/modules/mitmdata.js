const mitmdata = {
  state: {
    dataSource: []
  },
  mutations: {
    saveUserMitmData(state, payload) {
      state.dataSource = payload;
    },
    // 清除用户mitmproxy
    removeUserMitmData(state) {
      state.dataSource = [];
    }
  }
};

export default mitmdata;
