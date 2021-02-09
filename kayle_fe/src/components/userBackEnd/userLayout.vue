<template>
  <div id="logo">
    <div class="usermodel">
      <img src="@/assets/kaylehead.jpg" class="logoImg" />
      <span class="spanTitle">KAYLE</span>
      <p style="margin-top: 20px;">
        KAYLE 是一款致力于提升灰度回归质量的QA测试平台
      </p>
    </div>
    <router-view></router-view>
    <!-- <div>
      ccc
      <router-link to="www.baidu.com" style="color:black;font-size:20px;"
        ><a-icon type="user"></a-icon>wiki</router-link
      >
    </div>
    <div>
      问题反馈
    </div> -->
  </div>
</template>

<script></script>

<style scoped>
@media (min-width: 900px) {
  .iconLogo {
    font-size: 60px;
  }
  .spanTitle {
    font-size: 35px;
    margin-left: 20px;
    color: black;
  }
}

@media (max-width: 900px) {
  .iconLogo {
    font-size: 30px;
  }
  .spanTitle {
    font-size: 25px;
    margin-left: 10px;
  }
}

.usermodel {
  margin-top: 50px;
}

#logo {
  background: url("../../assets/kaylebe.jpeg");
  background-size: 100% 100%;
  height: 100%;
  position: fixed;
  width: 100%;
  text-align: center;
}

.logoImg {
  height: 70px;
  width: 70px;
  border-radius: 35px;
}
</style>
