<template>
  <div>
    <a-modal
      v-model="sonVisible"
      title="核心接口编辑"
      @ok="onSubmit"
      width="600px"
      okText="保存"
      @cancel="resetForm"
      cancelText="取消"
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
          label="接口正则"
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
          <a-select v-model="form.belongBusiness" placeholder="请选择所属业务">
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
          <a-input v-model="form.interfaceDesc" type="textarea" />
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
import { message } from "ant-design-vue";
import request from "@/utils/request";
import { belongBusiness } from "@/utils/commonconfig";

export default {
  data() {
    return {
      sonVisible: false,
      labelCol: { span: 4 },
      wrapperCol: { span: 14 },
      belongBusiness: belongBusiness,
      form: {
        interfacePath: "",
        interfaceRegular: "",
        belongBusiness: "Other",
        interfaceDesc: ""
      },
      rules: {
        interfacePath: [
          { required: true, message: "请输入核心接口路径", trigger: "blur" },
          {
            min: 3,
            max: 100,
            message: "接口路径为3～100个字符长度",
            trigger: "blur"
          }
        ],
        interfaceRegular: [
          { required: true, message: "请输入接口匹配正则", trigger: "blur" },
          {
            min: 3,
            max: 100,
            message: "接口匹配正则长度为3～100个字符",
            trigger: "blur"
          }
        ],
        belongBusiness: [
          {
            required: true,
            message: "请选择所属业务",
            trigger: "change",
            defaultValue: "Other"
          }
        ],
        interfaceDesc: [
          { required: true, message: "请输入核心接口描述", trigger: "blur" }
        ]
      }
    };
  },
  // 这里要使用一个监听属性，检测父属性visible的变化
  watch: {
    visible() {
      this.sonVisible = this.visible;
    },
    nowColumns() {
      this.form.interfacePath = this.nowColumns.interfacePath;
      this.form.interfaceRegular = this.nowColumns.interfaceRegular;
      this.form.belongBusiness = this.nowColumns.content;
      this.form.interfaceDesc = this.nowColumns.interfaceDesc;
    }
  },
  props: ["visible", "nowColumns"],
  methods: {
    onSubmit() {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          this.nowColumns.interfacePath = this.form.interfacePath;
          this.nowColumns.interfaceRegular = this.form.interfaceRegular;
          this.nowColumns.belongBusiness = this.form.belongBusiness;
          this.nowColumns.interfaceDesc = this.form.interfaceDesc;

          request({
            url: "/api/tempinter/editcore",
            method: "POST",
            data: this.nowColumns
          }).then(res => {
            if (res.data.code === 260000) {
              message.success(res.data.msg);
            } else {
              message.error(res.data.msg);
            }
          });
        } else {
          return false;
        }
      });

      this.$emit("changeShowEditModol", {
        visible: false,
        reload: true
      });
    },
    resetForm() {
      this.$refs.ruleForm.resetFields();
      this.$emit("changeShowEditModol", {
        visible: false,
        reload: true
      });
    }
  }
};
</script>

<style></style>
