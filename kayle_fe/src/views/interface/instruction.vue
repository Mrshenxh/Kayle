<template>
  <div>
    <a-page-header
      style="border: 1px solid rgb(235, 237, 240)"
      title="使用说明"
      sub-title="各个模块详细使用规范"
      :avatar="{ props: routes }"
    >
      <template slot="extra">
        <a-button
          key="1"
          type="primary"
          @click="
            pushToIntermodule(
              'http://wiki.in.zhihu.com/pages/viewpage.action?pageId=179948584',
              true
            )
          "
        >
          详细教程
        </a-button>
      </template>
    </a-page-header>
    <br />
    <div>
      <a-steps :current="current" @change="onChange" style="margin-top:10px;">
        <a-step title="Step 1" description="连接mitmproxy代理" />
        <a-step title="Step 2" description="接口上传接口列表" />
        <a-step title="Step 3" description="创建版本回归计划" />
        <a-step title="Step 4" description="实时查看接口覆盖率" />
      </a-steps>
      <a-divider />
      <div style="background:#ECECEC; padding:30px">
        <div v-show="div1">
          <a-row :span="24">
            <a-col :span="8">
              <a-card title="创建代理" :bordered="false" style="width: 300px">
                <p style="font-size: 16px">
                  <iconfont iconType="icon-ziyuan3"></iconfont>
                  <span style="font-size: 14px"
                    >如果没有mitmproxy代理，点击“录制模式”，自动进入创建代理页面</span
                  >
                </p>
                <p style="font-size: 16px">
                  <iconfont iconType="icon-2"></iconfont>
                  <span style="font-size: 14px"
                    >创建代理页面，输入端口号，要抓取的host，代理时间，点击确认</span
                  >
                </p>
                <p style="font-size: 16px">
                  <iconfont iconType="icon-3"></iconfont>
                  <span style="font-size: 14px"
                    >创建成功之后，手机连接相应的<span style="color:red"
                      >IP</span
                    >和<span style="color:red">端口号</span>(同Charles)</span
                  >
                </p>
              </a-card>
            </a-col>
            <a-col :span="8">
              <a-card title="mitm证书" :bordered="false" style="width: 300px">
                <p style="font-size: 16px">
                  <iconfont iconType="icon-ziyuan3"></iconfont>
                  <span style="font-size: 14px"
                    >手机连接代理之后，浏览器访问http://mitm.it地址</span
                  >
                </p>
                <p style="font-size: 16px">
                  <iconfont iconType="icon-2"></iconfont>
                  <span style="font-size: 14px"
                    >进入证书下载页面后，选择相应<span style="color:red"
                      >设备系统</span
                    >的pem或者cer进行下载</span
                  >
                </p>
                <p style="font-size: 16px">
                  <iconfont iconType="icon-3"></iconfont>
                  <span style="font-size: 14px"
                    >下载安装完毕之后，按照操作指引信任证书，此过程同Charles</span
                  >
                </p>
              </a-card>
            </a-col>
            <a-col :span="8">
              <a-card title="其他&问题" :bordered="false" style="width: 300px">
                <p style="font-size: 16px">
                  <iconfont iconType="icon-ziyuan3"></iconfont>
                  <span style="font-size: 14px"
                    >证书安装成功后，重新杀进程查看是否可以抓取到https的数据</span
                  >
                </p>
                <p style="font-size: 16px">
                  <iconfont iconType="icon-2"></iconfont>
                  <span style="font-size: 14px"
                    >Android部分机型访问网址没有出现证书下载，建议使用第三方浏览器重试</span
                  >
                </p>
                <p style="font-size: 16px">
                  <iconfont iconType="icon-3"></iconfont>
                  <span style="font-size: 14px"
                    >使用完毕，建议及时关闭代理，系统也会根据代理有效时间进行清理</span
                  >
                </p>
              </a-card>
            </a-col>
          </a-row>
        </div>

        <div v-show="div2">
          <a-card :bordered="false" style="width: calc(100%);" title="接口上传">
            <p style="font-size: 16px">
              1、抓取找到需要上传的核心功能接口，点击“上传接口”按钮，正常弹出上传接口弹窗。
            </p>
            <p style="font-size: 16px">
              2、核心接口弹窗，需要上传的字段有接口地址，接口正则表达式，接口所属业务，接口描述等。
            </p>
            <p class="spaceSpan" style="font-size: 16px">
              需要注意点:
              <br />
              <iconfont iconType="icon-ziyuan3"></iconfont>
              接口正则表达式目的为匹配的接口有且只有一则数据，更多学习请参考<a
                @click="
                  pushToIntermodule(
                    'http://tools.jb51.net/regex/create_reg',
                    true
                  )
                "
                >正则学习地址</a
              >。
              <br />
              <iconfont iconType="icon-2"></iconfont>
              请务必填写详细的接口描述，如是进入某个页面哪些元素，某个弹窗的数据接口，方便后续维护🙏。
            </p>
            <p style="font-size: 16px">
              3、接口正常上传成功之后，即可在<span
                @click="pushToIntermodule('/interface/intermodule', false)"
                class="interGet"
                >接口列表</span
              >查看最新上传接口。
            </p>
          </a-card>
        </div>

        <div v-show="div3">
          <a-card :bordered="false" style="width: calc(100%);" title="计划创建">
            <p style="font-size: 16px">
              1、如果没有计划，正常展示计划未创建页面，用户可以查看历史计划。
            </p>
            <p style="font-size: 16px">
              2、历史计划中，可以查看到之前计划的详细信息，包括创建人，创建时间，覆盖率，接口信息等。
            </p>
            <p style="font-size: 16px">
              3、创建版本计划时，需要填写相应的测试版本，业务范围，开始时间和结束时间。
            </p>
            <p class="spaceSpan" style="font-size: 16px">
              字段说明:
              <br />
              <iconfont iconType="icon-ziyuan3"></iconfont
              >测试版本：即回归包测试的版本，如7.3.0版本，正常写7.3.0即可，记住不要有空格或者其他字符
              。
              <br />
              <iconfont iconType="icon-2"></iconfont>
              业务范围：选择了业务范围之后，则计划会添加业务范围下所有接口纳入回归覆盖当中。
              <br />
              <iconfont iconType="icon-3"></iconfont>
              开始/结束时间：计划会在此时间段内进行数据采集，结束时间后，计划自动置于已结束，并归档到历史计划。
            </p>
          </a-card>
        </div>

        <div v-show="div4">
          <p>
            计划创建成功之后，手机连接代理，正常回归测试，则就会把数据匹配，修改覆盖率
          </p>
          <img
            src="../../assets/planImg.jpg"
            alt="测试计划覆盖率"
            style="width:calc(100%);"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import iconfont from "@/components/modulelist/iconfont";

export default {
  data() {
    return {
      current: 0,
      div1: true,
      div2: false,
      div3: false,
      div4: false,
      routes: {
        icon: "notification",
        size: "default"
      }
    };
  },
  components: {
    iconfont
  },
  methods: {
    onChange(current) {
      console.log("onChange:", current);
      this.current = current;
      if (this.current === 0) {
        this.div1 = true;
        this.div2 = false;
        this.div3 = false;
        this.div4 = false;
      } else if (this.current === 1) {
        this.div1 = false;
        this.div2 = true;
        this.div3 = false;
        this.div4 = false;
      } else if (this.current === 2) {
        this.div1 = false;
        this.div2 = false;
        this.div3 = true;
        this.div4 = false;
      } else {
        this.div1 = false;
        this.div2 = false;
        this.div3 = false;
        this.div4 = true;
      }
    },
    pushToIntermodule(pathLink, isBlank) {
      if (!isBlank) {
        this.$router.push(pathLink);
        return;
      }
      // let routeData = this.$router.resolve({
      //   path: pathLink,
      // });
      window.open(pathLink, "_blank");
    }
  }
};
</script>

<style>
tr:last-child td {
  padding-bottom: 0;
}

.spaceSpan {
  text-indent: 2em;
}

.interGet {
  color: blue;
}

.interGet:hover {
  cursor: pointer;
  color: red;
  /*光标呈现为指示链接的指针（一只手）*/
}
</style>
