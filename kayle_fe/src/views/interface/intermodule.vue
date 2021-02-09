<template>
  <div>
    <a-page-header
      title="核心接口"
      sub-title="所有用户上传的接口列表"
      :avatar="{ props: routes }"
    >
    </a-page-header>

    <a-form
      class="ant-advanced-search-form"
      :form="form"
      style="margin-left:20px"
    >
      <a-row :gutter="24">
        <a-col :span="8">
          <a-form-item label="URL查询">
            <a-input
              placeholder="输入要接口URL信息"
              v-decorator="[`urlcontent`]"
            ></a-input>
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="所属业务">
            <a-select
              style="width: 180px"
              v-decorator="['belongBusiness']"
              placeholder="选择接口所属业务"
            >
              <a-select-option
                v-for="(item, index) in belongBusiness"
                :key="index"
                :value="item.busValue"
              >
                {{ item.busName }}
              </a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
        <a-col :span="4" :style="{ textAlign: 'right' }">
          <a-button type="primary" @click="handleSearch">
            搜索
          </a-button>
          <a-button :style="{ marginLeft: '8px' }" @click="handleReset">
            清空
          </a-button>
        </a-col>
      </a-row>
    </a-form>

    <a-table
      :columns="columns"
      :data-source="data"
      :scroll="{ x: 1500, y: 600 }"
      :pagination="pagination"
      @change="changePage"
      bordered
    >
      <div slot="belongBusiness" slot-scope="text, record">
        <a-tag :color="returnBusColor(record)">
          {{ record.content }}
        </a-tag>
      </div>

      <div slot="action" slot-scope="text, record">
        <a @click="clickEdit(record)"><a-icon type="edit"></a-icon> 编辑</a>
        <br />
        <a @click="showDeleteConfirm(record)"
          ><a-icon type="delete"></a-icon> 删除</a
        >
      </div>
    </a-table>

    <editmodal
      :visible="editVisible"
      :nowColumns="selectCoreData"
      @changeShowEditModol="changeEdits"
    ></editmodal>
  </div>
</template>
<script>
import request from "@/utils/request";
import { message, Modal } from "ant-design-vue";
import editmodal from "@/components/modulelist/editmodal";
import { belongBusiness, getBusinessColor } from "@/utils/commonconfig";

const columns = [
  {
    title: "接口path",
    width: 300,
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
    title: "接口ID",
    dataIndex: "interfaceId",
    key: "interfaceId",
    width: 150,
    scopedSlots: { customRender: "request-data" }
  },
  {
    title: "负责人",
    dataIndex: "userName",
    key: "userName",
    width: 100,
    scopedSlots: { customRender: "user-name" }
  },
  {
    title: "所属业务",
    dataIndex: "content",
    key: "content",
    width: 100,
    scopedSlots: { customRender: "belongBusiness" }
  },
  {
    title: "接口正则",
    dataIndex: "interfaceRegular",
    key: "interfaceRegular",
    width: 300
  },
  { title: "接口描述", dataIndex: "interfaceDesc", key: "interfaceDesc" },
  {
    title: "更多操作",
    key: "operation",
    fixed: "right",
    width: 100,
    scopedSlots: { customRender: "action" }
  }
];

export default {
  data() {
    return {
      data: [],
      columns: columns,
      coreInterUrl: "/api/tempinter/getcoreinter?pageid=1",
      deleteCoreUrl: "/api/tempinter/deletecore",
      belongBusiness: belongBusiness,
      pagination: {
        total: 10
      },
      form: this.$form.createForm(this, { name: "advanced_search" }),
      editVisible: false,
      selectCoreData: {},
      routes: {
        icon: "api",
        size: "large",
        style: "color: #f56a00; backgroundColor: red"
      }
    };
  },
  created() {
    request({
      url: this.coreInterUrl,
      method: "GET"
    }).then(res => {
      if (res.data.code === 230003) {
        console.log(res.data.data.data);
        this.data = res.data.data.data;
        this.pagination.total = res.data.data.totolPage * 10;
      }
    });
  },
  components: {
    editmodal
  },

  methods: {
    /**
     * changePage: 当分页变化时，触发的方法
     * e.current: 当前页的pageid
     * e.total: 一共多少条数据
     * e.pageSize: 每页有多少条数据
     */
    changePage(e) {
      var subStr = new RegExp(/pageid=\d{0,3}/);
      this.coreInterUrl = this.coreInterUrl.replace(
        subStr,
        "pageid=" + e.current
      );
      request({
        url: this.coreInterUrl,
        method: "GET"
      }).then(res => {
        if (res.data.code === 230003) {
          console.log(res.data.data.data);
          this.data = res.data.data.data;
          this.pagination.total = res.data.data.totolPage * 10;
        }
      });
    },
    clickEdit(record) {
      this.selectCoreData = record;
      this.editVisible = true;
    },

    changeEdits(params) {
      this.editVisible = params.visible;
      if (params.reload) {
        request({
          url: this.coreInterUrl,
          method: "GET"
        }).then(res => {
          if (res.data.code === 230003) {
            console.log(res.data.data.data);
            this.data = res.data.data.data;
            this.pagination.total = res.data.data.totolPage * 10;
          }
        });
      }
    },

    handleDeleteOk() {
      const interfaceDetail = {
        interfaceId: this.selectCoreData.interfaceId
      };
      request({
        url: this.deleteCoreUrl,
        method: "POST",
        data: interfaceDetail
      }).then(res => {
        if (res.data.code === 250000) {
          message.success(res.data.msg);
          request({
            url: this.coreInterUrl,
            method: "GET"
          }).then(res => {
            if (res.data.code === 230003) {
              console.log(res.data.data.data);
              this.data = res.data.data.data;
              this.pagination.total = res.data.data.totolPage * 10;
            }
          });
        } else {
          message.warning(res.data.msg);
        }
      });
    },

    getEndReqUrl(values) {
      this.coreInterUrl = "/api/tempinter/getcoreinter?pageid=1";
      if (values.urlcontent && values.belongBusiness) {
        this.coreInterUrl =
          this.coreInterUrl +
          "&urlcontent=" +
          values.urlcontent +
          "&belongBusiness=" +
          values.belongBusiness;
      } else if (values.urlcontent && !values.belongBusiness) {
        this.coreInterUrl =
          this.coreInterUrl + "&urlcontent=" + values.urlcontent;
      } else if (!values.urlcontent && values.belongBusiness) {
        this.coreInterUrl =
          this.coreInterUrl + "&belongBusiness=" + values.belongBusiness;
      }
    },

    handleSearch() {
      this.form.validateFields((error, values) => {
        console.log("Received values of form: ", values);
        this.getEndReqUrl(values);
        request({
          url: this.coreInterUrl,
          method: "GET"
        }).then(res => {
          if (res.data.code === 230003) {
            this.data = res.data.data.data;
            this.pagination.total = res.data.data.totolPage * 10;
          }
        });
      });
    },

    handleReset() {
      this.form.resetFields();
      this.coreInterUrl = "/api/tempinter/getcoreinter?pageid=1";
      message.success("已经为您清空了所有搜索条件");
    },
    showDeleteConfirm(record) {
      this.selectCoreData = record;
      const that = this;
      Modal.confirm({
        title: "确认要删除此接口么？(删除之后不可恢复)",
        content: record.interfacePath,
        okText: "确认",
        okType: "danger",
        cancelText: "取消",
        onOk() {
          that.handleDeleteOk();
        },
        onCancel() {
          console.log("Cancel");
        }
      });
    },

    returnBusColor(record) {
      return getBusinessColor(record.content);
    }
  }
};
</script>
<style scoped>
.ant-advanced-search-form .ant-form-item {
  display: flex;
}
</style>
