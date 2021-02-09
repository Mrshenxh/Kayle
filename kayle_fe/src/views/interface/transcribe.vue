<template>
  <div v-cloak>
    <createmitm v-show="createShow" @create-event="getCreateData"></createmitm>
    <div id="components-form-demo-advanced-search" v-show="has_mitmproxy">
      <a-form
        class="ant-advanced-search-form"
        :form="form"
        @submit="handleSearch"
      >
        <a-row :gutter="24">
          <a-col :span="8">
            <a-form-item label="URL查询">
              <a-input
                placeholder="输入要查询URL信息"
                v-decorator="[`urlcontent`]"
              ></a-input>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="应用查询">
              <a-input
                placeholder="输入URL所属应用"
                v-decorator="[`applyname`]"
              ></a-input>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="请求方式">
              <a-select
                v-decorator="['selectMethod']"
                mode="multiple"
                placeholder="筛选请求method"
                class="search-methdod-select"
              >
                <a-select-option value="GET">
                  GET
                </a-select-option>
                <a-select-option value="POST">
                  POST
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        <a-row>
          <a-col :span="12" :style="{ textAlign: 'left' }">
            <a-button type="primary" @click="clearAllDataSource"
              >清除全部</a-button
            >
          </a-col>
          <a-col :span="12" :style="{ textAlign: 'right' }">
            <a-button type="primary" html-type="submit">
              添加搜索规则
            </a-button>
            <a-button :style="{ marginLeft: '8px' }" @click="handleReset">
              清空搜索规则
            </a-button>
            <!-- <a :style="{ marginLeft: '8px', fontSize: '12px' }" @click="toggle">
            Collapse <a-icon :type="expand ? 'up' : 'down'" />
          </a> -->
            <a-button
              type="primary"
              @click="closemitmproxy"
              :style="{ marginLeft: '8px', fontSize: '12px' }"
              >关闭mitmproxy</a-button
            >
          </a-col>
        </a-row>
      </a-form>

      <div class="search-result-list">
        <draggable
          :columns="columns"
          :rowSelection="rowSelection"
          ref="draggable"
        ></draggable>
      </div>
      <!-- <a-form :style="{ marginTop: '8px' }">
        <a-form-item>
          <a-row>
            <a-col :span="24" :style="{ textAlign: 'right' }">
              <a-button
                type="primary"
                :style="{ marginLeft: '8px' }"
                @click="clickScreen"
                >{{ screenText }}</a-button
              >
              <a-button
                type="primary"
                :style="{ marginLeft: '8px' }"
                :disabled="true"
                >确认</a-button
              >
            </a-col>
          </a-row>
        </a-form-item>
      </a-form> -->
    </div>
  </div>
</template>

<script>
// 录制上传页面

import request from "@/utils/request";
import createmitm from "@/components/modulelist/createmitm";
import { message } from "ant-design-vue";
import draggable from "@/components/modulelist/draggable";
import { hostIp } from "@/utils/commonconfig";

const columns = [
  {
    title: "接口path",
    width: 350,
    dataIndex: "interfacePath",
    key: "interfacePath",
    scopedSlots: { customRender: "interface-path" }
  },
  {
    title: "请求方式",
    width: 100,
    dataIndex: "requestMethod",
    key: "requestMethod"
  },
  {
    title: "请求数据",
    dataIndex: "requestData",
    key: "requestData",
    width: 300,
    scopedSlots: { customRender: "request-data" }
  },
  // { title: '请求Header', dataIndex: 'requestHeader', key: 'requestHeader', width: 200 , scopedSlots: { customRender: 'request-header',},},
  // { title: '请求耗时', dataIndex: 'requestTime', key: '3', width: 100 },
  // {
  //   title: "Status",
  //   dataIndex: "responseStatus",
  //   key: "responseStatus",
  //   width: 100
  // },
  // { title: '返回Header', dataIndex: 'responseHeader', key: 'responseHeader', width: 200 , scopedSlots: { customRender: 'response-header',},},
  {
    title: "返回Data",
    dataIndex: "responseData",
    key: "responseData",
    scopedSlots: { customRender: "response-data" }
  },
  // { title: '请求Size', dataIndex: 'requestSize', key: '7', width: 100 },
  // { title: '返回Size', dataIndex: 'responseSize', key: '8' },
  {
    title: "Action",
    key: "operation",
    fixed: "right",
    width: 100,
    scopedSlots: { customRender: "action" }
  }
];

const rowSelection = {
  onChange: (selectedRowKeys, selectedRows) => {
    console.log(
      `selectedRowKeys: ${selectedRowKeys}`,
      "selectedRows: ",
      selectedRows
    );
  },
  onSelect: (record, selected, selectedRows) => {
    console.log(record, selected, selectedRows);
  },
  onSelectAll: (selected, selectedRows, changeRows) => {
    console.log(selected, selectedRows, changeRows);
  }
};

export default {
  data() {
    return {
      columns: columns,
      expand: false,
      form: this.$form.createForm(this, { name: "advanced_search" }),
      socket: "",
      has_mitmproxy: false,
      createShow: true,
      mitm_message: {},
      isEdited: false,
      index: 0,
      selectCondition: {}
    };
  },
  components: {
    createmitm,
    draggable
  },
  computed: {
    count() {
      return this.expand ? 11 : 7;
    },

    // 添加筛选row相关策略
    rowSelection() {
      return this.isEdited ? rowSelection : null;
    },
    // 筛选/取消筛选按钮切换
    screenText() {
      return this.isEdited ? "取消筛选" : "筛选";
    }
  },
  updated() {
    console.log("updated");
  },
  destroyed() {
    if (this.socket !== "") {
      // 销毁监听
      this.socket.onclose = this.close;
    }
  },
  created() {
    // 在创建时候就请求查询是否有对应的port
    console.log(this.$store.state.mitmproxy);
    console.log(this.$store.state.auth);
    if (
      sessionStorage.getItem("mitmproxy") &&
      this.$store.state.mitmproxy !== undefined &&
      "port" in this.$store.state.mitmproxy &&
      this.$store.state.mitmproxy.port !== ""
    ) {
      this.createShow = false;
      this.has_mitmproxy = true;
      this.webSocketInit();
    } else {
      this.$store.dispatch({ type: "getUserMitmproxy" }).then(res => {
        console.log(res);
        if (res === 230000) {
          this.createShow = true;
          this.has_mitmproxy = false;
        } else if (res === 230002) {
          this.createShow = false;
          this.has_mitmproxy = true;
          this.webSocketInit();
        }
      });
    }
  },
  methods: {
    // 点击搜索按钮，触发方法
    handleSearch(e) {
      e.preventDefault();
      this.form.validateFields((error, values) => {
        console.log("error", error);
        console.log("Received values of form: ", values);
        this.selectCondition = values;
        this.$refs.draggable.dataSource = [];
        this.index = 0;
        message.success("已经为您添加了接口筛选条件");
      });
    },
    // 如果userid为空，则手动再次请求以下
    webSocketInit() {
      request({
        url: "/api/user/message",
        method: "POST"
      }).then(res => {
        if (res.data.code === 120000) {
          this.init(
            "ws://" +
              hostIp +
              "/tempinter/tempsocket/flow/" +
              res.data.data.user_id
          );
        } else {
          message.error("无法获取到websocket连接:" + res.data.code);
        }
      });
    },
    // 点击清空按钮，触发方法
    handleReset() {
      this.form.resetFields();
      this.selectCondition = {};
      message.success("已经为您删除了所有筛选条件");
    },
    // 搜索选项折叠
    toggle() {
      this.expand = !this.expand;
    },
    //点击删除全部，清空所有表格数据
    clearAllDataSource() {
      this.$refs.draggable.dataSource = [];
      this.index = 0;
    },
    getCreateData(data) {
      // 这个时候组件已经创建成功
      this.mitm_message = data;
      console.log("走到回调方法啦");
      console.log(this.$store.state.mitmproxy.port);
      if (
        this.$store.state.mitmproxy.port !== "" &&
        this.$store.state.mitmproxy.mitm_id !== ""
      ) {
        console.log("进入判断");
        if (this.socket === "") {
          this.webSocketInit();
        }
        this.createShow = false;
        this.has_mitmproxy = true;
      }
    },

    init: function(websocketPath) {
      if (typeof WebSocket === "undefined") {
        alert("您的浏览器不支持socket");
      } else {
        this.socket = new WebSocket(websocketPath);
        // 监听socket连接
        this.socket.onopen = this.open;
        // 监听socket错误信息
        this.socket.onerror = this.error;
        // 监听socket消息
        this.socket.onmessage = this.getMessage;
      }
    },
    open: function() {
      console.log("socket连接成功");
    },
    error: function() {
      console.log("连接错误");
    },
    // 获取到数据之后，将数据填充给 子组件的dataSource
    getMessage: function(msg) {
      var eachData = JSON.parse(msg.data);
      // console.log(msg.data);
      var totalEachData = {
        key: this.index,
        interfacePath: eachData.req_url,
        expireTime: eachData.expire_time,
        mitmId: eachData.mitm_id,
        reqStart: eachData.req_start,
        reqEnd: eachData.req_end,
        resStart: eachData.res_start,
        resEnd: eachData.res_end,
        userId: eachData.user_id,
        requestMethod: eachData.req_method,
        requestData: eachData.json_text,
        requestQuery: eachData.get_data,
        requestForm: eachData.post_data,
        requestScheme: eachData.req_scheme,
        requestHeader: eachData.req_header,
        requestCookie: eachData.req_cookie,
        responseCookie: eachData.res_cookie,
        responseStatus: eachData.res_status_code,
        responseHeader: eachData.res_header,
        responseData: eachData.res_text,

        popoverStatus: {
          interfacePath: {
            visiable: false,
            clickVisiable: false
          },
          requestData: {
            visiable: false,
            clickVisiable: false
          },
          requestHeader: {
            visiable: false,
            clickVisiable: false
          },
          responseHeader: {
            visiable: false,
            clickVisiable: false
          },
          responseData: {
            visiable: false,
            clickVisiable: false
          }
        }
      };

      if (
        this.selectCondition.urlcontent !== undefined &&
        totalEachData.interfacePath.search(this.selectCondition.urlcontent) ===
          -1
      ) {
        return;
      }

      if (
        this.selectCondition.applyname !== undefined &&
        totalEachData.interfacePath.search(this.selectCondition.applyname) ===
          -1
      ) {
        return;
      }

      if (
        this.selectCondition.selectMethod !== undefined &&
        this.selectCondition.selectMethod.indexOf(
          totalEachData.requestMethod
        ) === -1
      ) {
        return;
      }
      if (this.$refs.draggable) {
        this.$refs.draggable.dataSource.push(totalEachData);
        this.index += 1;
      }
    },
    send: function() {
      this.socket.send("haha");
    },
    close: function() {
      console.log("socket已经关闭");
    },
    closemitmproxy() {
      request({
        url: "/api/tempinter/stopmitm",
        method: "POST"
      }).then(res => {
        if (res.data.code === 220000) {
          message.success("已经为您关闭mitmproxy代理");
        } else if (res.data.code === 220002) {
          message.warning("查询到你这边没有对应的mitmproxy代理");
        }
        this.$store.dispatch({ type: "deleteUserMitmproxy" });
        this.socket.onclose = this.close;
      });
    },
    // 点击筛选/取消筛选按钮
    clickScreen() {
      console.log("clickScreen");
      this.isEdited = !this.isEdited;
    }
  }
};
</script>

<style scoped lang="less">
[v-cloak] {
  display: none;
}

.ant-advanced-search-form {
  padding: 24px;
  background: #fbfbfb;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
}

.ant-advanced-search-form .ant-form-item {
  display: flex;
}

.ant-advanced-search-form .ant-form-item-control-wrapper {
  flex: 1;
}

#components-form-demo-advanced-search .ant-form {
  max-width: none;
}
#components-form-demo-advanced-search {
  margin-top: 16px;
  border: 1px dashed #e9e9e9;
  border-radius: 6px;
  background-color: #fafafa;
  min-height: 200px;
  text-align: center;
  /* padding-top: 10px; */
}

.search-result-list {
  margin-top: 16px;
  border: 1px dashed #e9e9e9;
  border-radius: 6px;
  background-color: #fafafa;
  min-height: 200px;
  text-align: center;
  padding-top: 20px;
}

@media (min-width: 900px) {
  .search-methdod-select {
    width: 150px;
  }
}

@media (max-width: 900px) {
  .search-methdod-select {
    width: 100px;
  }
}
</style>
