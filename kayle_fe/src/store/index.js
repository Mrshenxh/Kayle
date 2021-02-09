import Vue from "vue";
import Vuex from "vuex";
import auth from "@/store/modules/auth";
import mitmproxy from "@/store/modules/mitmproxy";
import mitmdata from "@/store/modules/mitmdata";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    auth,
    mitmproxy,
    mitmdata
  }
});
