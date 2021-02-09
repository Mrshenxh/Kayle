<template>
  <div>
    <a-modal
      v-model="sonVisible"
      title="核心接口上传"
      @ok="handleUpload"
      okText="确认上传"
      @cancel="handleCancel"
      cancelText="取消上传"
    >
      <a-form-model
        ref="ruleForm"
        :model="form"
        :rules="rules"
        :label-col="labelCol"
        :wrapper-col="wrapperCol"
      >
        <a-form-model-item
          ref="interfacePath"
          label="接口名称"
          prop="interfacePath"
        >
          <a-input
            v-model="form.interfacePath"
            @blur="
              () => {
                $refs.interfacePath.onFieldBlur();
              }
            "
          />
        </a-form-model-item>

        <a-form-model-item
          ref="interfaceRegular"
          label="匹配正则"
          prop="interfaceRegular"
        >
          <a-input
            v-model="form.interfaceRegular"
            @blur="
              () => {
                $refs.interfaceRegular.onFieldBlur();
              }
            "
          />
        </a-form-model-item>

        <a-form-model-item label="所属业务" prop="belongBusiness">
          <a-select
            v-model="form.belongBusiness"
            placeholder="请选择接口所属业务线"
          >
            <a-select-option
              v-for="(item, index) in belongBusiness"
              :key="index"
              :value="item.busValue"
            >
              {{ item.busName }}
            </a-select-option>
          </a-select>
        </a-form-model-item>

        <a-form-model-item label="接口描述" prop="interfaceDesc">
          <a-input
            v-model="form.interfaceDesc"
            type="textarea"
            placeholder="请输入对接口的描述，如所属功能块"
          />
        </a-form-model-item>
      </a-form-model>
      <div>
        <a-tabs default-active-key="1">
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
    </a-modal>
  </div>
</template>
<script>
import request from "@/utils/request";
import { message } from "ant-design-vue";
import { belongBusiness } from "@/utils/commonconfig";

// 核心接口上传modal
export default {
  data() {
    /**
     * sonVisible: 弹窗是否可见
     * labelCol，wrapperCol: 每一个Item所占长度比例分布
     * form: 表单数据
     * rules: 表单校验规则
     */
    return {
      sonVisible: false,
      labelCol: { span: 4 },
      wrapperCol: { span: 14 },
      belongBusiness: belongBusiness,
      form: {
        interfacePath: "",
        interfaceRegular: "",
        belongBusiness: undefined,
        interfaceDesc: ""
      },
      rules: {
        interfacePath: [
          { required: true, message: "请输入接口路径", trigger: "blur" },
          {
            min: 10,
            max: 200,
            message: "接口路径限制在10～200个字符",
            trigger: "blur"
          }
        ],
        interfaceRegular: [
          { required: true, message: "请输入接口匹配正则", trigger: "blur" },
          {
            min: 10,
            max: 200,
            message: "接口匹配正则限制在5～100个字符",
            trigger: "blur"
          }
        ],
        belongBusiness: [
          { required: true, message: "请选择接口所属业务线", trigger: "change" }
        ],
        interfaceDesc: [
          { required: true, message: "请输入接口描述信息", trigger: "blur" }
        ]
      }
    };
  },
  props: ["visible", "nowColumns"],
  // 这里要使用一个监听属性，检测父属性visible的变化
  watch: {
    visible() {
      this.sonVisible = this.visible;
    },
    nowColumns() {
      this.form.interfacePath = this.nowColumns.interfacePath;
    }
  },
  methods: {
    /**
     * handleUpload: 上传接口
     * handleCancel: 点击取消请求接口
     * resetForm: 重置form表单数据
     */
    handleUpload(e) {
      console.log(e);
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          const values = {
            ...this.nowColumns,
            ...this.form
          };
          request({
            url: "/api/tempinter/uploadcoreinter",
            method: "POST",
            data: values
          }).then(res => {
            if (res.data.code === 200000) {
              message.success(res.data.msg);
            } else if (res.data.code === 200002) {
              message.error(res.data.msg);
            } else {
              message.error(res.data.msg);
            }
          });
        } else {
          return false;
        }
      });
      this.$emit("changeUploadPop", false);
    },
    handleCancel(e) {
      console.log(e);
      this.$emit("changeUploadPop", false);
    },

    resetForm() {
      this.$refs.ruleForm.resetFields();
    }
  }
};
</script>
