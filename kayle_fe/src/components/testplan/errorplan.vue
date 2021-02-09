<template>
  <div>
    <div v-show="showErrorView">
      <a-page-header title="回归计划" sub-title="版本迭代回归计划">
        <template slot="tags">
          <a-tag :color="baseTag.tagColor">
            {{ baseTag.tagTitle }}
          </a-tag>
        </template>
        <template slot="extra">
          <a-button key="3" @click="showHistoryPlan">
            历史计划
          </a-button>
        </template>
      </a-page-header>
      <a-empty :description="localErrorMessage" style="padding: 20px;">
        <span slot="description"> {{ localErrorMessage }} </span>
        <a-button type="primary" @click="createPlan" v-show="createShow">
          新建计划
        </a-button>
      </a-empty>
    </div>
    <historyplan
      v-show="showHistoryView"
      @closeHistory="closePlanList"
    ></historyplan>
  </div>
</template>

<script>
import historyplan from "@/components/testplan/historyplan";

export default {
  data() {
    return {
      localErrorMessage: "",
      baseTag: {
        tagTitle: "",
        tagColor: ""
      },
      createShow: false,
      showErrorView: true,
      showHistoryView: false
    };
  },
  props: ["planStatus"],
  created() {
    console.log("haah");
    console.log(this.planStatus);
  },
  components: {
    historyplan
  },
  watch: {
    planStatus() {
      if (this.planStatus === 310001) {
        this.localErrorMessage = "创建失败，请稍后再试";
        this.baseTag.tagTitle = "已失败";
        this.baseTag.tagColor = "red";
        this.createShow = false;
      } else if (this.planStatus === 310002) {
        this.localErrorMessage = "计划创建中，请稍后刷新查看";
        this.baseTag.tagTitle = "创建中";
        this.baseTag.tagColor = "coral";
        this.createShow = false;
      } else if (this.planStatus === 310003) {
        this.localErrorMessage = "计划等待中，请稍后刷新查看";
        this.baseTag.tagTitle = "等待中";
        this.baseTag.tagColor = "gray";
        this.createShow = false;
      } else if (this.planStatus === 310004) {
        this.localErrorMessage = "暂无已创建计划，请操作创建";
        this.baseTag.tagTitle = "未创建";
        this.baseTag.tagColor = "cornflowerblue";
        this.createShow = true;
      }
    }
  },
  methods: {
    createPlan() {
      this.$emit("errorEmit");
    },
    showHistoryPlan() {
      console.log("showHistoryPlan");
      this.showErrorView = false;
      this.showHistoryView = true;
    },
    closePlanList() {
      console.log("closeHistoryPlan");
      this.showErrorView = true;
      this.showHistoryView = false;
    }
  }
};
</script>

<style></style>
