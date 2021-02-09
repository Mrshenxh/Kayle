<template>
  <div>
    <a-modal
      v-model="sonVisible"
      title="接口详情"
      @ok="handleOk"
      width="1000px"
      okText="确认"
      @cancel="handleCancel"
      cancelText="取消"
    >
      <template>
        <div style="background-color: #ececec; padding: 20px;">
          <a-row :gutter="8">
            <a-col :span="8">
              <a-card title="接口状态" :bordered="false" style="height:300px">
                <p>接口路径: {{ nowColumns.interfacePath }}</p>
                <p>请求方式: {{ nowColumns.requestMethod }}</p>
                <p>请求状态: {{ nowColumns.responseStatus }}</p>
              </a-card>
            </a-col>
            <a-col :span="8">
              <a-card title="接口耗时" :bordered="false" style="height:300px">
                <p>请求开始: {{ nowColumns.reqStart }}</p>
                <p>请求结束: {{ nowColumns.reqEnd }}</p>
                <p>返回开始: {{ nowColumns.resStart }}</p>
                <p>返回结束: {{ nowColumns.resEnd }}</p>
              </a-card>
            </a-col>
            <a-col :span="8">
              <a-card title="用户相关" :bordered="false" style="height:300px">
                <p>用户ID: {{ nowColumns.userId }}</p>
                <p>MitmID: {{ nowColumns.mitmId }}</p>
                <p>代理失效时间: {{ nowColumns.expireTime }}</p>
              </a-card>
            </a-col>
          </a-row>
        </div>
        <div>
          <a-tabs default-active-key="1" @change="callback" type="card">
            <a-tab-pane key="1" tab="请求Header">
              <json-viewer
                :value="nowColumns.requestHeader"
                copyable
                boxed
                sort
              ></json-viewer>
            </a-tab-pane>
            <a-tab-pane key="2" tab="请求Data">
              <json-viewer
                :value="nowColumns.requestData"
                copyable
                boxed
                sort
              ></json-viewer>
            </a-tab-pane>
            <a-tab-pane key="3" tab="返回Header" force-render>
              <json-viewer
                :value="nowColumns.responseHeader"
                copyable
                boxed
                sort
              ></json-viewer>
            </a-tab-pane>
            <a-tab-pane key="4" tab="返回Response">
              <json-viewer
                :value="nowColumns.responseData"
                copyable
                boxed
                sort
              ></json-viewer>
            </a-tab-pane>
          </a-tabs>
        </div>
      </template>
    </a-modal>
  </div>
</template>
<script>
export default {
  data() {
    return {
      sonVisible: false
    };
  },
  props: ["visible", "nowColumns"],
  // 这里要使用一个监听属性，检测父属性visible的变化
  watch: {
    visible() {
      this.sonVisible = this.visible;
    }
  },
  methods: {
    // 点击OK调用方法
    handleOk(e) {
      console.log(e);
      this.$emit("changeShowEachModol", false);
    },
    //点击取消调用方法
    handleCancel(e) {
      console.log(e);
      this.$emit("changeShowEachModol", false);
    },
    // 切换Tab时候回调的方法
    callback(key) {
      console.log(key);
    }
  }
};
</script>
