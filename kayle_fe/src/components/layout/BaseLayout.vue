<template>
  <a-layout id="components-layout-demo-side" style="min-height: 100vh">
    <a-layout-sider v-model="collapsed" :trigger="null">
      <div class="logo">
        <img src="@/assets/kaylehead.jpg" class="logoImg" />
        <span style="margin-left:5px;" v-if="fontShow">KAYLE</span>
      </div>
      <SliderMenu></SliderMenu>
    </a-layout-sider>

    <a-layout>
      <a-layout-header class="baseHeader">
        <a-icon
          :type="iconType"
          class="trigger"
          @click="collapsed = !collapsed"
        ></a-icon>
        <Header></Header>
      </a-layout-header>

      <a-layout-content style="margin: 0 16px">
        <a-breadcrumb style="margin: 16px 0">
          <a-breadcrumb-item v-for="(item, index) in routeName" :key="index">{{
            item
          }}</a-breadcrumb-item>
        </a-breadcrumb>
        <div
          :style="{ padding: '24px', background: '#fff', minHeight: '360px' }"
        >
          <router-view></router-view>
        </div>
      </a-layout-content>

      <a-layout-footer style="text-align: center">
        QA Test Platform, 致力于轻松你的工作
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>
<script>
import Header from "@/components/layout/Header";
import SliderMenu from "@/components/layout/SliderMenu";
import getAllSliderRouter from "@/utils/getrouter.js";
export default {
  data() {
    return {
      collapsed: false
    };
  },
  computed: {
    iconType() {
      console.log(this.routeName);
      if (this.collapsed) {
        return "menu-unfold";
      } else {
        return "menu-fold";
      }
    },
    fontShow() {
      console.log(this.routeName);
      if (this.collapsed) {
        return false;
      } else {
        return true;
      }
    },
    routeName() {
      const sliderRoute = getAllSliderRouter(this);
      console.log(sliderRoute);
      let routePathList = this.$route.path.split("/");
      let returnArray = new Array();
      for (let index = 0; index < routePathList.length; index++) {
        const pathName = routePathList[index];
        const pathChinaName = this.getPathName(sliderRoute, pathName);
        if (pathChinaName) {
          returnArray.push(pathChinaName);
        }
      }
      return returnArray;
    }
  },
  components: {
    Header,
    SliderMenu
  },
  methods: {
    getPathName(needArray, pathName) {
      let returnName = "";
      for (let index = 0; index < needArray.length; index++) {
        const element = needArray[index];
        if (element.name === pathName) {
          return element.meta.title;
        } else if (element.children) {
          returnName = this.getPathName(element.children, pathName);
          if (returnName) {
            break;
          }
        }
      }
      return returnName;
    }
  }
};
</script>

<style scoped>
#components-layout-demo-side .logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  margin: 16px;
}

.trigger {
  padding: 0 20px;
  line-height: 64px;
  font-size: 20px;
}
.trigger:hover {
  background: white;
}

.logo {
  height: 64px;
  line-height: 32px;
  text-align: center;
  overflow: hidden;
  color: #ffffff;
  white-space: pre;
}

.logoImg {
  height: 30px;
  width: 30px;
  border-radius: 15px;
}

.baseHeader {
  background: #fff;
  padding: 0;
}
</style>
