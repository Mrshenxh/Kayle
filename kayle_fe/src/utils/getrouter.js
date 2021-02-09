export default function getAllSliderRouter(baselayout) {
  const totalRoute = baselayout.$router.options.routes;
  let sliderMenu = Object;
  for (let index = 0; index < totalRoute.length; index++) {
    const eachRoute = totalRoute[index];
    if (eachRoute.name && eachRoute.name === "slidermenu") {
      sliderMenu = eachRoute.children;
      break;
    }
  }
  // 获取到所有侧边栏的数据
  for (let index = 0; index < sliderMenu.length; index++) {
    if (
      sliderMenu[index].meta &&
      sliderMenu[index].meta.icon &&
      sliderMenu[index].meta.title
    ) {
      continue;
    }
    sliderMenu.splice(index, 1);
  }
  return sliderMenu;
}
