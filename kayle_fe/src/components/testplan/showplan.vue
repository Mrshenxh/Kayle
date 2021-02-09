<template>
  <div>
    <div>
      <a-page-header
        title="回归计划"
        :sub-title="basePlanDetail.clientVersion + '版本回归测试计划'"
      >
        <template slot="tags">
          <a-tag color="blue">
            执行中
          </a-tag>
        </template>
        <template slot="extra">
          <a-button key="3">
            修改计划
          </a-button>
          <a-button key="2" @click="showDeleteConfirm">
            关闭计划
          </a-button>
          <a-button key="1" type="primary">
            重启计划
          </a-button>
        </template>
        <a-row type="flex" style="padding: 10px;">
          <a-statistic title="测试版本" :value="basePlanDetail.clientVersion" />
          <a-statistic
            title="创建人"
            :value="basePlanDetail.planUser"
            :style="{
              margin: '0 35px'
            }"
          />
          <a-statistic
            title="覆盖率"
            :value="basePlanDetail.coreRate"
            :value-style="{ color: 'red' }"
            :style="{
              margin: '0 35px'
            }"
          />
          <a-statistic
            title="开始时间"
            :value="basePlanDetail.planStart"
            :style="{
              margin: '0 35px'
            }"
            value-style="font-size:18px;margin-top:10px"
          />
          <a-statistic
            title="结束时间"
            :value="basePlanDetail.planEnd"
            :style="{
              margin: '0 35px'
            }"
            value-style="font-size:18px;margin-top:10px"
          />
        </a-row>
      </a-page-header>
    </div>
    <div>
      <a-tabs default-active-key="1" @change="changeTab">
        <a-tab-pane key="1">
          <span slot="tab">
            <a-icon type="file" />
            所有接口
          </span>
          <plantable
            :columns="columns"
            :tabType="tabtype"
            :usersearch="usersearch"
          ></plantable>
        </a-tab-pane>

        <a-tab-pane key="2">
          <span slot="tab">
            <a-icon type="undo" />
            未匹配接口
          </span>
          <plantable
            :columns="columns"
            :tabType="tabtype"
            :usersearch="usersearch"
          ></plantable>
        </a-tab-pane>
        <a-input-search
          slot="tabBarExtraContent"
          enter-button
          placeholder="请输入负责人名称"
          style="width: 200px"
          @search="onSearch"
        />
      </a-tabs>
    </div>
  </div>
</template>

<script>
import request from "@/utils/request";
import { message, Modal } from "ant-design-vue";
import plantable from "@/components/testplan/plantable";

export default {
  data() {
    return {
      basePlanDetail: {
        clientVersion: "",
        planUser: "",
        coreRate: "",
        planStart: "",
        planEnd: "",
        coreData: []
      },
      columns: [
        {
          title: "接口正则",
          dataIndex: "interface_regular",
          key: "interface_regular",
          width: 300,
          scopedSlots: { customRender: "interface_regular" }
        },
        {
          title: "接口ID",
          dataIndex: "interface_id",
          key: "interface_id",
          width: 200
        },
        {
          title: "负责人",
          dataIndex: "user_name",
          key: "user_name",
          width: 100
        },
        {
          title: "所属业务",
          dataIndex: "content",
          key: "content",
          width: 100,
          scopedSlots: { customRender: "belongBusiness" }
        },
        {
          title: "接口描述",
          dataIndex: "interface_desc",
          key: "interface_desc"
        }
      ],
      usersearch: "",
      tabtype: "coreData"
    };
  },
  props: ["planDetail"],
  components: {
    plantable
  },
  watch: {
    planDetail() {
      this.basePlanDetail = this.planDetail;
    }
  },
  methods: {
    closePlan() {
      request({
        url: "/api/plan/stopplan",
        method: "POST"
      }).then(res => {
        if (res.data.code === 320000) {
          message.success(res.data.msg);
          /**
           * 计划创建成功，回调给父组件
           */
          this.$emit("closedPlan");
        } else {
          message.warning(res.data.msg);
        }
      });
    },
    showDeleteConfirm() {
      const that = this;
      Modal.confirm({
        title: "确认要关闭此计划么？",
        content: that.basePlanDetail.clientVersion + "版本回归测试计划",
        okText: "确认",
        okType: "danger",
        cancelText: "取消",
        onOk() {
          that.closePlan();
        },
        onCancel() {
          console.log("Cancel");
        }
      });
    },
    onSearch(value) {
      console.log(value);
      this.usersearch = value;
    },
    changeTab(activityKey) {
      console.log(activityKey);
      if (activityKey === "1") {
        this.tabtype = "coreData";
      } else if (activityKey === "2") {
        this.tabtype = "unDoneCore";
      }
    }
  }
};
</script>
<style>
tr:last-child td {
  padding-bottom: 0;
  /* color:cornflowerblue */
}
</style>
