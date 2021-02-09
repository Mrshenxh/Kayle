<template>
  <div>
    <div v-show="showPlanList">
      <a-page-header
        title="历史计划"
        @back="() => this.$emit('closeHistory')"
      />
      <a-list
        class="demo-loadmore-list"
        :loading="loading"
        item-layout="horizontal"
        :data-source="data"
      >
        <div
          v-if="showLoadingMore"
          slot="loadMore"
          :style="{
            textAlign: 'center',
            marginTop: '12px',
            height: '32px',
            lineHeight: '32px'
          }"
        >
          <a-spin v-if="loadingMore" />
          <a-button v-else @click="getPlanData()">
            loading more
          </a-button>
        </div>
        <a-list-item slot="renderItem" slot-scope="item">
          <a slot="actions" @click="clickPlanDetail(item)">查看详情</a>
          <a slot="actions" @click="showDeleteConfirm(item)">删除计划</a>
          <a-list-item-meta :description="planDetailContent(item)">
            <a slot="title" href="https://www.antdv.com/"
              >版本: {{ item.clientVersion }}</a
            >
            <iconfont
              style="font-size:30px"
              slot="avatar"
              iconType="icon-plan1"
            ></iconfont>
          </a-list-item-meta>
          <!-- <div>创建人: {{ item.planUser }}</div> -->
        </a-list-item>
      </a-list>
    </div>

    <eachhistoryplan
      v-show="showEachPlan"
      ref="eachhistoryplan"
      @closeHistoryDetail="reShowPlanList"
    ></eachhistoryplan>
  </div>
</template>
<script>
import request from "@/utils/request";
import { message, Modal } from "ant-design-vue";
import iconfont from "@/components/modulelist/iconfont";
import eachhistoryplan from "@/components/testplan/eachhistoryplan";

export default {
  data() {
    return {
      loading: false,
      loadingMore: false,
      showLoadingMore: true,
      data: [],
      baseUrl: "/api/plan/historyplan?pageid=",
      pageIndex: 1,
      showPlanList: true,
      showEachPlan: false
    };
  },
  created() {
    this.getPlanData();
  },
  watch: {},
  components: {
    iconfont,
    eachhistoryplan
  },
  methods: {
    getPlanData() {
      this.loadingMore = true;
      const total_req = this.baseUrl + this.pageIndex;
      request({
        url: total_req,
        method: "GET"
      }).then(res => {
        if (res.data.code === 340000) {
          this.data = [...this.data, ...res.data.data.data];
          console.log(this.data);
          if (this.pageIndex >= res.data.data.totolPage) {
            this.showLoadingMore = false;
          }
        } else {
          message.warning(res.data.msg);
        }
        this.pageIndex += 1;
        this.loadingMore = false;
      });
    },

    planDetailContent(record) {
      return (
        "接口覆盖率：" + record.coreRate + "；计划创建人：" + record.planUser
      );
      //   return "开始时间：" + record.planStart + "；结束时间："+ record.planEnd + "；覆盖率：" + record.coreRate;
    },

    handleDeleteOk(record) {
      console.log(record);
      request({
        url: "/api/plan/deletehistoryplan",
        method: "POST",
        data: { id: record.id }
      }).then(res => {
        if (res.data.code === 350000) {
          message.success(res.data.msg);
          /**
           * 删除成功后，将数据重置
           */
          this.pageIndex = 1;
          this.data = [];
          this.showLoadingMore = true;
          this.getPlanData();
        } else {
          message.warning(res.data.msg);
        }
      });
    },
    showDeleteConfirm(record) {
      this.selectCoreData = record;
      const that = this;
      Modal.confirm({
        title: "确认要删除此接口么？(删除之后不可恢复)",
        content:
          "版本: " + record.clientVersion + "; 创建人: " + record.planUser,
        okText: "确认",
        okType: "danger",
        cancelText: "取消",
        onOk() {
          that.handleDeleteOk(record);
        },
        onCancel() {
          console.log("Cancel");
        }
      });
    },
    clickPlanDetail(record) {
      console.log(record.id);
      this.$refs.eachhistoryplan.getPlanId(record);
      this.showPlanList = false;
      this.showEachPlan = true;
    },
    reShowPlanList() {
      this.showEachPlan = false;
      this.showPlanList = true;
    }
  }
};
</script>
<style>
.demo-loadmore-list {
  min-height: 350px;
}
</style>
