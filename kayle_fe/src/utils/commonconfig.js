var limitHostList = ["api.zhihu.com", "www.zhihu.com"];

var belongBusiness = [
  {
    busName: "内容&会员",
    busValue: "Content",
    busColor: "volcano"
  },
  {
    busName: "其他",
    busValue: "Other",
    busColor: "green"
  },
  {
    busName: "教育",
    busValue: "Education",
    busColor: "red"
  }
];
// 本地
// var hostIp = "10.14.12.28:3334";
// 线上
var hostIp = "10.101.1.51:3334";

function getBusinessColor(busValue) {
  for (let index = 0; index < belongBusiness.length; index++) {
    const element = belongBusiness[index];
    if (element.busValue === busValue) {
      return element.busColor;
    }
  }
  return "grey";
}

export { limitHostList, belongBusiness, hostIp, getBusinessColor };
