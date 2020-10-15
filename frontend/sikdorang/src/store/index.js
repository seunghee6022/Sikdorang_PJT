import Vue from "vue";
import Vuex from "vuex";
import VueCookies from "vue-cookies";

Vue.use(Vuex);
Vue.use(VueCookies);

import mapEvent from "./modules/mapEvent.js";
import mypage from "./modules/mypage.js";
import schedule from "./modules/schedule.js";
import themes from "./modules/themes.js";
import order from "./modules/order.js";
import sikRec from "./modules/sikRec.js";
import party from "./modules/party.js";
import vuexPersistedstate from "vuex-persistedstate";
import SecureLS from "secure-ls";

var ls = new SecureLS({ isCompression: false });

export default new Vuex.Store({
  state: {
    positions: [],
    isLogin: !!window.$cookies.get("auth-token"),
    // SERVER_URL: "http://j3d202.p.ssafy.io:3000/",
    SERVER_URL: 'http://localhost:8080/',
    // IMG_SERVER_URL: "http://j3d202.p.ssafy.io:3000",
    IMG_SERVER_URL: 'http://localhost:8080',
    LOCAL_URL: "http://j3d202.p.ssafy.io:8181/project/sikdorang",
    TOUR_API_KEY : "secret",
      KAKAO_MAP_API_KEY : "secret",
  },
  mutations: {},
  actions: {},
  modules: {
    mypage: mypage,
    mapEvent,
    schedule,
    themes,
    order,
    sikRec,
    party,
  },
  plugins: [
    vuexPersistedstate({
      storage: {
        getItem: (key) => ls.get(key),
        setItem: (key, value) => ls.set(key, value),
        removeItem: (key) => ls.remove(key),
      },
    }),
  ],
});
