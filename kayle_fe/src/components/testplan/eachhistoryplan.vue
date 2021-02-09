<template>
  <div>
    <div>
      <a-page-header
        title="回归计划"
        :sub-title="basePlanDetail.clientVersion + '版本回归测试计划'"
        @back="() => this.$emit('closeHistoryDetail')"
      >
        <template slot="tags">
          <a-tag color="grey">
            已结束
          </a-tag>
        </template>
        <a-row type="flex" style="padding: 10px;">
          <a-statistic title="测试版本" :value="basePlanDetail.clientVersion" />
          <a-statistic
            title="创建人"
            :value="basePlanDetail.planUser"
            :style="{
              margin: '0 35px'
            }"
          />
          <a-statistic
            title="覆盖率"
            :value="basePlanDetail.coreRate"
            :value-style="{ color: 'red' }"
            :style="{
              margin: '0 35px'
            }"
          />
          <a-statistic
            title="开始时间"
            :value="basePlanDetail.planStart"
            :style="{
              margin: '0 35px'
            }"
            value-style="font-size:18px;margin-top:10px"
          />
          <a-statistic
            title="结束时间"
            :value="basePlanDetail.planEnd"
            :style="{
              margin: '0 35px'
            }"
            value-style="font-size:18px;margin-top:10px"
          />
        </a-row>
      </a-page-header>
    </div>
    <historyplantable
      ref="historyplantable"
      :planId="planId"
    ></historyplantable>
  </div>
</template>

<script>
import historyplantable from "@/components/testplan/historyplantable";

export default {
  data() {
    return {
      planId: 0,
      basePlanDetail: {
        clientVersion: "",
        planUser: "",
        coreRate: "",
        planStart: "",
        planEnd: ""
      }
    };
  },
  watch: {
    planId() {
      console.log(this.planId);
    }
  },
  components: {
    historyplantable
  },
  created() {
    console.log("enter created");
    console.log(this.id);
  },
  props: ["id"],
  methods: {
    getPlanId(record) {
      this.planId = record.id;
      this.basePlanDetail = { ...record };
      console.log(this.basePlanDetail);
      this.$refs.historyplantable.baseRequestFunc(this.planId, 1);
    }
  }
};
</script>

<style></style>
