<template>
  <div>
    <a-table
      :columns="columns"
      :data-source="dataSource"
      :scroll="{ x: 1500, y: 800 }"
      :rowSelection="rowSelection"
      bordered
    >
      <div slot="interface-path" slot-scope="text, record">
        <a-tooltip
          style="width: 200px"
          title="点击查看完整URL"
          trigger="hover"
          :visible="
            getSomeoneInterFaceIsVisible(
              getDataSourceIndexByRecordKey(record.key),
              'interfacePath',
              'visiable'
            )
          "
          @visibleChange="
            handleHoverChange(
              getDataSourceIndexByRecordKey(record.key),
              'interfacePath'
            )
          "
        >
          <a-popover
            title="接口路径"
            trigger="click"
            :visible="
              getSomeoneInterFaceIsVisible(
                getDataSourceIndexByRecordKey(record.key),
                'interfacePath',
                'clickVisiable'
              )
            "
            @visibleChange="handleClickChange(record.key, 'interfacePath')"
          >
            <div slot="content">
              <div>
                {{
                  dataSource[getDataSourceIndexByRecordKey(record.key)]
                    .interfacePath
                }}
              </div>
              <a @click="hide(record.key, 'interfacePath')">Close</a>
            </div>
            <p
              v-if="
                JSON.stringify(
                  dataSource[getDataSourceIndexByRecordKey(record.key)]
                    .interfacePath
                ).length > 50
              "
            >
              {{
                JSON.stringify(
                  dataSource[getDataSourceIndexByRecordKey(record.key)]
                    .interfacePath
                ).substring(0, 50) + "..."
              }}
            </p>
            <p v-else>
              {{
                JSON.stringify(
                  dataSource[getDataSourceIndexByRecordKey(record.key)]
                    .interfacePath
                )
              }}
            </p>
          </a-popover>
        </a-tooltip>
      </div>

      <div slot="request-data" slot-scope="text, record">
        <a-popover
          title="接口请求参数"
          trigger="click"
          :visible="
            dataSource[record.key].popoverStatus.requestData.clickVisiable
          "
        >
          <div slot="content">
            <div>{{ dataSource[record.key].requestData }}</div>
            <a @click="hide(record.key, 'requestData')">Close</a>
          </div>
          <p
            v-if="
              JSON.stringify(dataSource[record.key].requestData).length > 50
            "
          >
            {{
              JSON.stringify(dataSource[record.key].requestData).substring(
                0,
                50
              ) + "..."
            }}
            <a @click="clickMore(record.key, 'requestData')">更多</a>
          </p>
          <p v-else>
            {{ JSON.stringify(dataSource[record.key].requestData) }}
          </p>
        </a-popover>
      </div>

      <div slot="response-data" slot-scope="text, record">
        <p
          v-if="JSON.stringify(dataSource[record.key].responseData).length > 50"
        >
          {{
            JSON.stringify(dataSource[record.key].responseData).substring(
              0,
              50
            ) + "..."
          }}
          <a @click="clickMore(record.key, 'responseData')">更多</a>
        </p>
        <p v-else>
          {{ JSON.stringify(dataSource[record.key].responseData) }}
        </p>
        <a-modal
          v-model="
            dataSource[record.key].popoverStatus.responseData.clickVisiable
          "
          title="接口返回数据"
          @ok="hide(record.key, 'responseData')"
          width="1000px"
        >
          <json-viewer
            :value="dataSource[record.key].responseData"
            copyable
            boxed
            sort
          ></json-viewer>
        </a-modal>
      </div>

      <div slot="action" slot-scope="text, record">
        <a @click="showMoreData(record.key)">查看详情</a>
        <a @click="showEachUploadPop(record.key)">上传接口</a>
      </div>
    </a-table>
    <listmodal
      :visible="isShowMore"
      :nowColumns="nowColumns"
      @changeShowEachModol="changeShowModol"
    ></listmodal>
    <uploadmodal
      :visible="showUpload"
      :nowColumns="nowColumns"
      @changeUploadPop="changeEachUploadPop"
    ></uploadmodal>
  </div>
</template>

<script>
import listmodal from "@/components/modulelist/listmodal";
import uploadmodal from "@/components/modulelist/uploadmodal";

export default {
  data() {
    return {
      /**
       * isShowMore: 检测是否要弹窗展示某个单独行的数据，供计算属性和子组件监听使用
       * nowColumns: 点击查看时，当前选中的dataSource column
       * dataSource: 重新定义数据接收参数 便于进行变更
       * showUpload: 是否要弹窗上传单条数据
       */
      isShowMore: false,
      showUpload: false,
      nowColumns: {},
      dataSource: []
    };
  },
  /**
   * 属性含义
   * columns: 列表第一行的值
   * rowSelection: 筛选状态下，用户选中行
   * */

  props: ["columns", "rowSelection"],
  components: {
    listmodal,
    uploadmodal
  },
  methods: {
    // 通过子组件listmodal回调改变isShowMore的值
    changeShowModol(params) {
      this.isShowMore = params;
    },
    changeEachUploadPop(params) {
      this.showUpload = params;
    },
    // cell中 点击“查看详情”方法调用
    showMoreData(recordKey) {
      this.isShowMore = true;
      this.nowColumns = this.dataSource[recordKey];
      console.log(this.nowColumns);
    },
    // cell中 点击“上传接口”方法调用
    showEachUploadPop(recordKey) {
      this.showUpload = true;
      this.nowColumns = this.dataSource[recordKey];
    },
    // 根据record.key获取当前数据在数组中的index
    getDataSourceIndexByRecordKey(recordKey) {
      for (let nowIndex = 0; nowIndex < this.dataSource.length; nowIndex++) {
        const nowElement = this.dataSource[nowIndex];
        if (nowElement.key === recordKey) {
          return nowIndex;
        }
      }
      return null;
    },
    /**
     * 方法定义: 获取某个接口字段是否可见
     * 接口字段定义
     * recordKey: 对应某个数据里的key
     * dataType: 对应接口字段，如“interfacePath”
     * clickOrHover: 手势操作，visiable和clickVisiable
     */
    getSomeoneInterFaceIsVisible(recordKey, dataType, clickOrHover) {
      const nowIndex = this.getDataSourceIndexByRecordKey(recordKey);
      if (nowIndex !== null) {
        return this.dataSource[nowIndex].popoverStatus[dataType][clickOrHover];
      }
    },

    // 点击“隐藏”方法调用
    hide(recordKey, attribute) {
      const nowIndex = this.getDataSourceIndexByRecordKey(recordKey);
      if (nowIndex !== null) {
        this.dataSource[nowIndex].popoverStatus[
          attribute
        ].clickVisiable = false;
      }
    },
    // 列表中点击“更多”方法调用
    clickMore(recordKey, attribute) {
      const nowIndex = this.getDataSourceIndexByRecordKey(recordKey);
      if (nowIndex !== null) {
        this.dataSource[nowIndex].popoverStatus[attribute].clickVisiable = true;
      }
    },
    // 分别通过手势和点击操作，将选中key对应的属性取反操作
    handleHoverChange(nowIndex, attribute) {
      if (
        attribute in this.dataSource[nowIndex].popoverStatus &&
        this.dataSource[nowIndex].popoverStatus[attribute].clickVisiable ===
          false
      ) {
        this.dataSource[nowIndex].popoverStatus[attribute].visiable = !this
          .dataSource[nowIndex].popoverStatus[attribute].visiable;
        console.log(
          this.dataSource[nowIndex].popoverStatus[attribute].visiable
        );
      }
    },
    handleClickChange(recordKey, attribute) {
      const nowIndex = this.getDataSourceIndexByRecordKey(recordKey);
      if (nowIndex !== null) {
        if (attribute in this.dataSource[nowIndex].popoverStatus) {
          this.dataSource[nowIndex].popoverStatus[
            attribute
          ].clickVisiable = !this.dataSource[nowIndex].popoverStatus[attribute]
            .clickVisiable;
          if (
            this.dataSource[nowIndex].popoverStatus[attribute].clickVisiable ===
            true
          ) {
            this.dataSource[nowIndex].popoverStatus[attribute].visiable = false;
          }
        }
      }
    }
  }
};
</script>

<style scoped lang="less"></style>
