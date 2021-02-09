<template>
  <div>
    <div v-show="showCreateView">
      <a-page-header title="创建计划" sub-title="没有在运行中的回归计划">
        <template slot="tags">
          <a-tag color="brown">
            未创建
          </a-tag>
        </template>
        <template slot="extra">
          <a-button key="3" @click="showHistoryPlan">
            历史计划
          </a-button>
        </template>
      </a-page-header>

      <a-row :gutter="8">
        <a-col :span="10">
          <a-form-model
            ref="ruleForm"
            :model="form"
            :rules="rules"
            :label-col="labelCol"
            :wrapper-col="wrapperCol"
            style="width:500px;padding: 20px;"
          >
            <a-form-model-item
              ref="clientVersion"
              label="测试版本"
              prop="clientVersion"
            >
              <a-input
                v-model="form.clientVersion"
                @blur="
                  () => {
                    $refs.clientVersion.onFieldBlur();
                  }
                "
              />
            </a-form-model-item>

            <a-form-model-item label="业务范围" prop="planBusiness">
              <a-select
                mode="tags"
                v-model="form.planBusiness"
                placeholder="请选择本次计划覆盖业务"
                @change="handleChange"
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

            <a-form-model-item label="开始时间" prop="planStart">
              <a-date-picker
                v-model="form.planStart"
                show-time
                type="date"
                placeholder="请选择开始时间"
                style="width: 100%;"
              />
            </a-form-model-item>

            <a-form-model-item label="结束时间" prop="planEnd">
              <a-date-picker
                v-model="form.planEnd"
                show-time
                type="date"
                placeholder="请选择结束时间"
                style="width: 100%;"
              />
            </a-form-model-item>

            <a-form-model-item :wrapper-col="{ span: 14, offset: 4 }">
              <a-button type="primary" @click="onSubmit">
                创建计划
              </a-button>
              <a-button style="margin-left: 10px;" @click="resetForm">
                重置数据
              </a-button>
            </a-form-model-item>
          </a-form-model>
        </a-col>
        <a-col :span="14">
          <a-card title="创建说明" style="width: 500px;margin-left:10px;">
            <div>
              <h4>测试版本</h4>
              输入本次匹配上传的版本号，如iOS回归包，版本为6.69.0-test;Android为6.69.0-beta，则填写6.69.0即可。
            </div>
            <br />
            <div>
              <h4>业务范围</h4>
              选择相关业务模块，则本次计划会覆盖业务模块下所有接口
            </div>
            <br />
            <div>
              <h4>开始/结束时间</h4>
              选择开始/结束时间，则本次计划会在此时间段内做覆盖采集
            </div>
          </a-card>
        </a-col>
      </a-row>
    </div>

    <historyplan
      v-show="showHistoryView"
      @closeHistory="closePlanList"
    ></historyplan>
  </div>
</template>

<script>
import request from "@/utils/request";
import { message } from "ant-design-vue";
import { belongBusiness } from "@/utils/commonconfig";
import historyplan from "@/components/testplan/historyplan";

export default {
  data() {
    return {
      sonVisible: false,
      labelCol: { span: 4 },
      wrapperCol: { span: 14 },
      showCreateView: true,
      showHistoryView: false,
      belongBusiness: belongBusiness,
      form: {
        clientVersion: "",
        planBusiness: [],
        planStart: "",
        planEnd: ""
      },
      rules: {
        clientVersion: [
          {
            required: true,
            message: "请输入本次回归计划版本",
            trigger: "blur"
          },
          {
            min: 3,
            max: 10,
            message: "计划版本为3～10个字符长度",
            trigger: "blur"
          }
        ],
        planBusiness: [
          {
            required: true,
            message: "请选择所属业务",
            trigger: "change",
            type: "array"
          }
        ],
        planStart: [
          { required: true, message: "请选择计划开始时间", trigger: "change" }
        ],
        planEnd: [
          { required: true, message: "请选择计划结束时间", trigger: "change" }
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
  components: {
    historyplan
  },
  props: ["visible", "nowColumns"],
  methods: {
    onSubmit() {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          const dataForm = {
            clientVersion: this.form.clientVersion,
            planBusiness: this.form.planBusiness,
            planStart: this.form.planStart.format("YYYY-MM-DD HH:mm:ss"),
            planEnd: this.form.planEnd.format("YYYY-MM-DD HH:mm:ss")
          };
          request({
            url: "/api/plan/createplan",
            method: "POST",
            data: dataForm
          }).then(res => {
            if (res.data.code === 300000) {
              message.success(res.data.msg);
              /**
               * 计划创建成功，回调给父组件
               */
              this.$emit("createdPlan", res.data.msg);
            } else {
              message.warning(res.data.msg);
            }
          });
        } else {
          return false;
        }
      });
    },
    resetForm() {
      this.$refs.ruleForm.resetFields();
    },
    handleChange(value) {
      console.log(`Selected: ${value}`);
    },
    showHistoryPlan() {
      console.log("showHistoryPlan");
      console.log("showHistoryPlan");
      this.showCreateView = false;
      this.showHistoryView = true;
    },
    closePlanList() {
      console.log("closeHistoryPlan");
      this.showCreateView = true;
      this.showHistoryView = false;
    }
  }
};
</script>

<style></style>
