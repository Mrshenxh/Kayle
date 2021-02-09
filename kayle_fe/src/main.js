import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import JsonViewer from "vue-json-viewer";
import {
  Button,
  Layout,
  Icon,
  Drawer,
  Radio,
  Menu,
  Form,
  Input,
  Select,
  Breadcrumb,
  Dropdown,
  Avatar,
  Tabs,
  Table,
  Divider,
  Tag,
  FormModel,
  Checkbox,
  Collapse,
  Col,
  Row,
  DatePicker,
  Card,
  Spin,
  message,
  Popover,
  Tooltip,
  Modal,
  Descriptions,
  Popconfirm,
  Switch,
  PageHeader,
  Statistic,
  Empty,
  List,
  Steps
} from "ant-design-vue";

Vue.config.productionTip = false;
Vue.use(Button);
Vue.use(Layout);
Vue.use(Icon);
Vue.use(Drawer);
Vue.use(Radio);
Vue.use(Menu);
// Vue.use(Auth);
Vue.use(Form);
Vue.use(Input);
Vue.use(Select);
Vue.use(Breadcrumb);
Vue.use(Dropdown);
Vue.use(Avatar);
Vue.use(Tabs);
Vue.use(Table);
Vue.use(Divider);
Vue.use(Tag);
Vue.use(FormModel);
Vue.use(Checkbox);
Vue.use(Collapse);
Vue.use(Col);
Vue.use(Row);
Vue.use(DatePicker);
Vue.use(Card);
Vue.use(Spin);
Vue.use(message);
Vue.use(Popover);
Vue.use(Tooltip);
Vue.use(Modal);
Vue.use(Descriptions);
Vue.use(Popconfirm);
Vue.use(Switch);
Vue.use(JsonViewer);
Vue.use(PageHeader);
Vue.use(Statistic);
Vue.use(Empty);
Vue.use(List);
Vue.use(Steps);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
