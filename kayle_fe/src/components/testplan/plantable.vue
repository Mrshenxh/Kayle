<template>
  <div>
    <a-spin :spinning="isSpinning" tip="Loading...">
      <a-table
        :columns="tabType === 'coreData' ? coreColumns : unDoneColumns"
        :data-source="data"
        :pagination="pagination"
        :scroll="{ y: 500, x: 1500 }"
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
import { getBusinessColor } from "@/utils/commonconfig";

export default {
  data() {
    return {
      data: [],
      queryplancore: "/api/plan/queryplancore?",
      pageid: 1,
      coreColumns: [],
      unDoneColumns: [],
      pagination: {
        total: 10
      },
      isSpinning: false
    };
  },
  props: ["columns", "tabType", "usersearch"],

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
    },
    usersearch() {
      this.baseUsersearch = this.usersearch;
      this.pageid = 1;
      this.baseRequestFunc(this.pageid);
    }
  },

  created() {
    console.log(this.columns);
    console.log(this.tabType);
    this.isSpinning = true;
    if (this.tabType === "coreData") {
      this.coreColumns.push({
        title: "匹配信息(系统、版本、机型)",
        dataIndex: "match_infomation",
        key: "match_infomation",
        scopedSlots: { customRender: "imatch-infomation" },
        width: 300
      });
      this.coreColumns.push({
        title: "是否完成",
        dataIndex: "is_finished",
        key: "is_finished",
        width: 100,
        // fixed: "right",
        scopedSlots: { customRender: "is-finished" }
      });
      this.coreColumns = [...this.columns, ...this.coreColumns];
      console.log(this.coreColumns);
    } else if (this.tabType === "unDoneCore") {
      this.unDoneColumns = this.columns;
    }
    this.baseRequestFunc(this.pageid);
    this.isSpinning = false;
  },
  methods: {
    getQueryPlanCoreURL(pageId) {
      var baseQueryUrl =
        this.queryplancore + "tabtype=" + this.tabType + "&pageid=" + pageId;
      if (this.baseUsersearch) {
        baseQueryUrl = baseQueryUrl + "&usersearch=" + this.baseUsersearch;
      }
      return baseQueryUrl;
    },
    baseRequestFunc(pageid) {
      request({
        url: this.getQueryPlanCoreURL(pageid),
        method: "GET"
      }).then(res => {
        if (res.data.code === 330000 || res.data.code === 330006) {
          console.log(res.data.data.data);
          console.log("haha");
          console.log(res.data.data.totalPages);
          this.data = res.data.data.data;
          this.pagination.total = res.data.data.totalPages * 10;
        } else {
          this.data = [];
        }
      });
    },
    /**
     * changePage: 当分页变化时，触发的方法
     * e.current: 当前页的pageid
     * e.total: 一共多少条数据
     * e.pageSize: 每页有多少条数据
     */
    changePage(e) {
      console.log(e);
      this.baseRequestFunc(e.current);
    },

    returnBusColor(record) {
      return getBusinessColor(record.content);
    }
  }
};
</script>
