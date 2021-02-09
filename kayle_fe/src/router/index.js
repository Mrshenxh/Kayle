import Vue from "vue";
import VueRouter from "vue-router";
import NProgress from "nprogress";
import "nprogress/nprogress.css";
import request from "@/utils/request";

// import store from "../store"

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "slidermenu",
    component: () =>
      import(
        /* webpackChunkName: "/slidermenu" */ "../components/layout/BaseLayout.vue"
      ),
    children: [
      {
        path: "/",
        redirect: "/interface/instruction"
      },
      // 先把其他操作注释掉
      // {
      //   path: "/casetab",
      //   name: "casetab",
      //   meta: { icon: "dashboard", title: "测试用例", requireAuth: true },
      //   component: { render: h => h("router-view") },
      //   children: [
      //     {
      //       path: "/casetab/caselist",
      //       name: "caselist",
      //       meta: { requireAuth: true, title: "用例列表" },
      //       component: () =>
      //         import(
      //           /* webpackChunkName: "/casetab" */ "../views/case/caselist"
      //         ),
      //       children: [
      //         {
      //           path: "/casetab/caselist",
      //           redirect: "/casetab/caselist/totalcase"
      //         },
      //         {
      //           path: "/casetab/caselist/totalcase",
      //           name: "totalcase",
      //           meta: { title: "总用例集", requireAuth: true },
      //           component: () =>
      //             import(
      //               /* webpackChunkName: "/casetab" */ "../views/case/caselist/totalcase.vue"
      //             )
      //         },
      //         {
      //           path: "/casetab/caselist/eachcase",
      //           name: "eachcase",
      //           meta: { title: "单用例集", requireAuth: true },
      //           component: () =>
      //             import(
      //               /* webpackChunkName: "/casetab" */ "../views/case/caselist/eachcase.vue"
      //             )
      //         }
      //       ]
      //     },
      //     {
      //       path: "/casetab/casecreate",
      //       name: "casecreate",
      //       meta: { title: "用例创建", requireAuth: true },
      //       component: () =>
      //         import(
      //           /* webpackChunkName: "/casetab" */ "../views/case/casecreate.vue"
      //         )
      //     }

      //     // {
      //     //   path: '/casetab/eachcase',
      //     //   name: 'eachcase',
      //     //   meta: {title: "单用例集", requireAuth:true},
      //     //   component:()=>
      //     //     import(/* webpackChunkName: "/casetab" */ "../views/case/eachcase.vue"),
      //     // },
      //   ]
      // },
      // {
      //   path: "/normal",
      //   name: "normal",
      //   meta: { icon: "form", title: "日常工具", requireAuth: true },
      //   component: { render: h => h("router-view") },
      //   children: [
      //     {
      //       path: "/normal/tools",
      //       name: "tools",
      //       meta: { title: "工具集合", requireAuth: true },
      //       component: () =>
      //         import(
      //           /* webpackChunkName: "/normal" */ "../views/normal/tools.vue"
      //         )
      //     }
      //   ]
      // },
      {
        path: "/interface",
        name: "interface",
        meta: { icon: "form", title: "接口录制", requireAuth: true },
        component: { render: h => h("router-view") },
        children: [
          {
            path: "/interface/instruction",
            name: "instruction",
            meta: { title: "使用说明", requireAuth: true },
            component: () =>
              import(
                /* webpackChunkName: "/normal" */ "../views/interface/instruction.vue"
              )
          },
          {
            path: "/interface/transcribe",
            name: "transcribe",
            meta: { title: "录制模式", requireAuth: true },
            component: () =>
              import(
                /* webpackChunkName: "/normal" */ "../views/interface/transcribe.vue"
              )
          },
          {
            path: "/interface/testplan",
            name: "testplan",
            meta: { title: "测试计划", requireAuth: true },
            component: () =>
              import(
                /* webpackChunkName: "/normal" */ "../views/interface/testplan.vue"
              )
          },
          {
            path: "/interface/intermodule",
            name: "intermodule",
            meta: { title: "接口列表", requireAuth: true },
            component: () =>
              import(
                /* webpackChunkName: "/normal" */ "../views/interface/intermodule.vue"
              )
          }
        ]
      }
    ]
  },
  {
    path: "*",
    name: "404",
    component: () =>
      import(/* webpackChunkName: "/" */ "../views/error/404.vue")
  },
  {
    path: "/user",
    name: "user",
    component: () =>
      import(
        /* webpackChunkName: "about" */ "../components/userBackEnd/userLayout.vue"
      ),
    children: [
      {
        path: "/user",
        redirect: "/user/login"
      },
      {
        path: "/user/login",
        name: "login",
        meta: { title: "登录" },
        component: () =>
          import(/* webpackChunkName: "/normal" */ "../views/User/Login.vue")
      },
      {
        path: "/user/register",
        name: "register",
        meta: { title: "注册" },
        component: () =>
          import(/* webpackChunkName: "/normal" */ "../views/User/Register.vue")
      }
    ]
  }
];

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location, onResolve, onReject) {
  if (onResolve || onReject)
    return originalPush.call(this, location, onResolve, onReject);
  return originalPush.call(this, location).catch(err => err);
};

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  if (to.path !== from.path) {
    NProgress.start();
  }
  request({
    url: "/api/user/checklogin",
    method: "POST"
  }).then(res => {
    console.log(res.data.code);
    if (res.data.code === 100004 || to.path === "/user/register") {
      next();
    } else {
      next({ path: "/user/login" });
    }
  });
  next();
});

router.afterEach(() => {
  NProgress.done();
});

export default router;
