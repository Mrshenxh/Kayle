<template>
  <div>
    <a-spin :spinning="isSpinning" tip="Loading...">
      <a-table
        :columns="columns"
        :data-source="data"
        :pagination="pagination"
        :scroll="{ y: 300, x: 1500 }"
        @change="changePage"
        bordered
      >
        <div slot="belongBusiness" slot-scope="text, record">
          <a-tag :color="returnBusColor(record)">
            {{ record.content }}
          </a-tag>
        </div>

        <div slot="interface_regular" slot-scope="text, record">
          <div>
            {{ record.interface_regular }}
          </div>
        </div>

        <div slot="imatch-infomation" slot-scope="text, record">
          <div
            v-for="(matchDict, index) in record.match_infomation"
            :key="index"
          >
            <a-avatar shape="square" icon="snippets" size="small" />
            <a-tag color="pink" style="margin-left:10px">
              {{ matchDict.inter_os }}
            </a-tag>
            <a-tag color="red">
              {{ matchDict.inter_release }}
            </a-tag>
            <a-tag color="orange">
              {{ matchDict.inter_brand }}
            </a-tag>
          </div>
        </div>

        <div slot="is-finished" slot-scope="text, record">
          <a-icon
            :type="record.is_finished ? 'check-circle' : 'close-circle'"
            theme="twoTone"
            style="font-size: 24px;margin-left:15px"
            :two-tone-color="record.is_finished ? 'green' : 'red'"
          ></a-icon>
        </div>
      </a-table>
    </a-spin>
  </div>
</template>
<script>
import request from "@/utils/request";
import { message } from "ant-design-vue";
import { getBusinessColor } from "@/utils/commonconfig";

export default {
  data() {
    return {
      data: [],
      queryplancore: "/api/plan/historyplan/",
      planId: 0,
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
        },
        {
          title: "匹配信息(系统、版本、机型)",
          dataIndex: "match_infomation",
          key: "match_infomation",
          scopedSlots: { customRender: "imatch-infomation" },
          width: 300
        },
        {
          title: "是否完成",
          dataIndex: "is_finished",
          key: "is_finished",
          width: 100,
          // fixed: "right",
          scopedSlots: { customRender: "is-finished" }
        }
      ],
      pagination: {
        total: 10
      },
      isSpinning: false
    };
  },

  watch: {
    // 监听tabType变化，如果有变化则重新请求
    tabType(val, oldVal) {
      console.log(val);
      console.log(oldVal);
      if (val !== oldVal) {
        this.pageid = 1;
        console.log("tabType");
        this.baseRequestFunc(this.pageid);
      }
    }
  },

  methods: {
    getQueryPlanCoreURL(planId, pageId) {
      var baseQueryUrl = this.queryplancore + planId + "?pageid=" + pageId;
      return baseQueryUrl;
    },
    baseRequestFunc(planId, pageId) {
      request({
        url: this.getQueryPlanCoreURL(planId, pageId),
        method: "GET"
      }).then(res => {
        if (res.data.code === 360000) {
          this.data = res.data.data.data;
          this.pagination.total = res.data.data.totalPages * 10;
        } else {
          this.data = [];
          message.warning(res.data.msg);
        }
        this.planId = planId;
      });
    },
    changePage(e) {
      console.log(e);
      this.baseRequestFunc(this.planId, e.current);
    },
    returnBusColor(record) {
      return getBusinessColor(record.content);
    }
  }
};
</script>
