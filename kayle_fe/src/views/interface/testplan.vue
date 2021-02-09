<template>
  <div>
    <a-spin :spinning="spinning">
      <createplan
        v-show="createVisible"
        @createdPlan="reloadBaseView"
      ></createplan>
      <showplan
        v-show="planVisible"
        :planDetail="planDetail"
        @closedPlan="reloadShowView"
      ></showplan>
      <errorplan
        v-show="errorVisible"
        :planStatus="planStatus"
        @errorEmit="reloadCreateView"
      ></errorplan>
    </a-spin>
  </div>
</template>

<script>
import createplan from "@/components/testplan/createplan";
import showplan from "@/components/testplan/showplan";
import errorplan from "@/components/testplan/errorplan";
import request from "@/utils/request";
// import {message} from 'ant-design-vue';

export default {
  data() {
    return {
      createVisible: false,
      planVisible: false,
      errorVisible: false,
      planDetail: undefined,
      planStatus: 0,
      spinning: false,
      baseQueryUrl: "/api/plan/queryplan"
    };
  },
  components: {
    createplan,
    showplan,
    errorplan
  },
  created() {
    /**
     *  创建时候，请求是否有测试计划
     */
    this.commonQuery(this.baseQueryUrl);
  },
  methods: {
    reloadBaseView(msg) {
      console.log(msg);
      this.createVisible = false;
      this.commonQuery(this.baseQueryUrl);
    },
    reloadShowView() {
      this.planVisible = false;
      this.commonQuery(this.baseQueryUrl);
    },
    reloadCreateView() {
      this.errorVisible = false;
      this.createVisible = true;
    },
    commonQuery(queryUrl) {
      this.spinning = true;
      request({
        url: queryUrl,
        method: "GET"
      }).then(res => {
        if (res.data.code === 310000) {
          this.planVisible = true;
          this.planDetail = res.data.data;
        } else {
          this.errorVisible = true;
          this.planStatus = res.data.code;
        }
        this.spinning = false;
      });
    }
  }
};
</script>

<style></style>
