<template>
  <a-spin :spinning="showSpin">
    <div class="total-rouad">
      <a-form
        v-bind="formItemLayout"
        :form="form"
        @submit="handleSubmit"
        style="width:calc(60%);float:left;"
      >
        <a-form-item class="label-select">
          <H4>创建mitmproxy代理</H4>
        </a-form-item>
        <a-form-item label="代理Port" class="host-select">
          <a-input
            placeholder="输入创建代理端口号，如8808"
            allow-clear
            @change="onChange"
            v-decorator="[
              'input-port',
              {
                rules: [
                  {
                    required: true,
                    message: '请输入要创建mitmproxy的端口号',
                    type: 'string'
                  }
                ]
              }
            ]"
          />
        </a-form-item>

        <a-form-item label="筛选host" class="host-select">
          <a-select
            v-decorator="[
              'select-multiple',
              {
                rules: [
                  {
                    required: true,
                    message: '请选择接口所属业务线',
                    type: 'array'
                  }
                ]
              }
            ]"
            mode="multiple"
            placeholder="请选择要筛选的host"
          >
            <a-select-option
              v-for="(item, index) in limitHostList"
              :key="index"
              :value="item"
            >
              {{ item }}
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="代理时间" class="host-select">
          <a-date-picker
            v-decorator="['date-time-picker', config]"
            show-time
            format="YYYY-MM-DD HH:mm:ss"
          />
        </a-form-item>
        <a-form-item
          :wrapper-col="{
            xs: { span: 24, offset: 0 },
            sm: { span: 16, offset: 8 }
          }"
          class="host-select"
        >
          <a-button type="primary" html-type="submit">
            创建
          </a-button>
        </a-form-item>
      </a-form>
      <div style="width:calc(40%);float:left;">
        <a-card title="创建说明" style="width: 300px">
          <a slot="extra" @click="clickToInstruction()">更多</a>
          <p>1、使用mitmproxy需要先创建一个属于自己的端口号来监听流量</p>
          <p>2、目前支持筛选指定host的流量，如api.zhihu.com</p>
          <p>
            3、使用代理结束后，可以主动销毁mitmproxy，系统也会根据有效时间定时销毁
          </p>
        </a-card>
      </div>
    </div>
  </a-spin>
</template>
<script>
import { message } from "ant-design-vue";
import request from "@/utils/request";
import { limitHostList } from "@/utils/commonconfig";

console.log("createmitm");
console.log(limitHostList);

export default {
  data() {
    return {
      formItemLayout: {
        labelCol: {
          xs: { span: 24 },
          sm: { span: 8 }
        },
        wrapperCol: {
          xs: { span: 24 },
          sm: { span: 16 }
        }
      },
      config: {
        rules: [
          { type: "object", required: true, message: "请选择一个代理有效时间" }
        ]
      },
      showSpin: false,
      limitHostList: limitHostList
    };
  },
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: "time_related_controls" });
  },
  methods: {
    handleSubmit(e) {
      e.preventDefault();
      this.form.validateFields((err, fieldsValue) => {
        if (err) {
          return;
        }
        this.showSpin = true;
        const values = {
          ...fieldsValue,
          host_list: fieldsValue["select-multiple"].toString(),
          port: fieldsValue["input-port"],
          expire_time: fieldsValue["date-time-picker"].format(
            "YYYY-MM-DD HH:mm:ss"
          )
        };
        console.log(fieldsValue["date-time-picker"]);
        console.log("Received values of form: ", values);
        request({
          url: "/api/tempinter/createmitm",
          method: "POST",
          data: values
        }).then(res => {
          if (res.data.code === 210002) {
            message.success(res.data.msg);
          } else if (res.data.code === 210003) {
            message.warning(res.data.msg);
          } else {
            message.error("未知错误，服务端发生异常");
          }
          this.$store.dispatch({ type: "getUserMitmproxy" }).then(() => {
            console.log("走这里么");
            this.showSpin = false;
            this.$emit("create-event", res.data.data);
          });
        });
      });
    },
    onChange(e) {
      console.log("走的这里？？？");
      console.log(e);
    },
    clickToInstruction() {
      this.$router.push("/interface/instruction");
    }
  }
};
</script>

<style scoped>
@media (min-width: 900px) {
  .host-select {
    width: calc(60%);
  }
  .label-select {
    margin-left: calc(10%);
  }
}

@media (max-width: 900px) {
  .host-select {
    width: calc(70%);
  }
}

.total-rouad {
  display: inline;
}

.example {
  text-align: center;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
  margin-bottom: 20px;
  padding: 30px 50px;
  margin: 20px 0;
}
</style>
