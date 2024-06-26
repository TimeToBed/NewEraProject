<template>
  <div class="w-full mx-auto">
    <div class="w-full" style="display:flex ;align-items:center">
      <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
      <div>
        <div>　高伟鹏</div>
        <div>　三年级十八班</div>
      </div>
      <!-- 这个空div将推动后面的元素到最右边 -->
      <div style="flex-grow: 1;"></div>
      <div>
        欢迎
      </div>
    </div>

    <div class="mt-6">
      <div class="flex flex-wrap">
        <div class="lg:flex-8 lg:max-w-2/3 w-full lg:mb-0 lg:pr-3.5 mb-6">
          <GradientLineChart />
        </div>
        <!-- <div class="lg:flex-4 lg:max-w-1/3 w-full lg:pl-3.5">
          <TotalBarChart :Datalist="data2" />
        </div> -->
      </div>
    </div>

    <div class="mt-6">
      <div class="flex flex-wrap">
        <div class="lg:flex-8 lg:max-w-2/3 w-full lg:mb-0 lg:pr-3.5">
          <PageVisitTable />
        </div>
        <div class="lg:flex-4 lg:max-w-1/3 w-full lg:pl-3.5">
          <SocialTrafficTable />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, inject, onMounted, computed } from 'vue'
import { AxiosInstance } from 'axios'
import vueDanmaku from 'vue3-danmaku'
interface StudentPerformance {
  "最近一次考试成绩": string | number;
  "上升幅度": string | number;
}

interface ExamDetails {
  "0-30分段学生数量": number;
  "30-60分段学生数量": number;
  "60-90分段学生数量": number;
  "90-120分段学生数量": number;
  "120-150分段学生数量": number;
  "学生数量": number;
  "学生成绩": { [studentId: string]: string | number };
  "已批改的数量": number;
  "平均成绩": number;
  "现代文阅读平均得分率": number;
  "古代诗文阅读平均得分率": number;
  "语言文字运用平均得分率": number;
  "写作平均得分率": number;
}

interface DataStructure {
  data_dict: {
    [examCode: string]: ExamDetails | {}; // 允许空对象以适应如"1113"这样的键
    "学生总数": number;
  };
  student_dict: {
    [studentId: string]: StudentPerformance;
    "进步人数占比": Number;
  };
}
// Components import
import AnalysisCard from 'modules/cards/views/components/AnalysisCard.vue'
import GradientLineChart from './components/GradientLineChart.vue'
import TotalBarChart from './components/TotalBarChart.vue'
import SocialTrafficTable from './components/SocialTrafficTable.vue'
import PageVisitTable from './components/PageVisitTable.vue'

// 使用axios进行数据获取
const axios = inject('axios') as AxiosInstance | undefined;
// 数据
const dataList = ref({});
const data1 = ref<number[]>([]);
const data2 = ref({});
const data3 = ref({});
const data4 = ref({});
// 定义获取数据的异步函数
const getDataList = async () => {
  if (!axios) {
    console.error("Axios instance not found");
    return;
  }

  try {
    const response = await axios.get(`exams/data_list/2/`);
    getData1(response.data);
    getData2(response.data);
    dataList.value = response.data; // 将获取的数据存储到响应式引用中
  } catch (error) {
    console.error("Error during HTTP request:", error);
  }
};

// 使用onMounted生命周期钩子在组件挂载时调用getDataList
onMounted(() => {
  getDataList();
});
// 从得到的Data里获取所有需要的数据
// 获取卡片所需数据:1.学生数量 2.考试次数 3.批改试卷量 4.进步人数占比
function getData1(e: DataStructure) {
  // 计算学生总数
  const totalStudentCount = e.data_dict['学生总数'];

  // 计算考试次数，不包括“学生总数”这一项
  const examCount = Object.keys(e.data_dict).length - 1; // 减去“学生总数”的键

  // 计算批改试卷量
  let correctedExamsCount = 0;
  for (const key in e.data_dict) {
    if (e.data_dict[key].hasOwnProperty('已批改的数量')) {
      correctedExamsCount += e.data_dict[key]['已批改的数量'];
    }
  }

  // 获取进步人数占比
  const improvementPercentage = e.student_dict['进步人数占比'];

  // 返回计算出的信息
  data1.value = [totalStudentCount, examCount, correctedExamsCount, improvementPercentage];
  return [totalStudentCount, examCount, correctedExamsCount, improvementPercentage,];
}
function getData2(e: DataStructure) {
  // 获取最近一次考试各个分段学生数量
  const student_count = e.data_dict
  // step1 获取考试列表
  const maxKey = Math.min(...Object.keys(student_count)
    .filter(key => /^\d+$/.test(key)) // 筛选出纯数字的键
    .map(Number)); // 转换为数字
  // step2 获取最近一次考试
  const maxExam = student_count[maxKey];
  //step3 提取学生分数分布
  const studentScoreDistribution = maxExam ? {
    "0-30分段学生数量": maxExam["0-30分段学生数量"],
    "30-60分段学生数量": maxExam["30-60分段学生数量"],
    "60-90分段学生数量": maxExam["60-90分段学生数量"],
    "90-120分段学生数量": maxExam["90-120分段学生数量"],
    "120-150分段学生数量": maxExam["120-150分段学生数量"],
  } : {}; // 如果找不到最大的考试对象，则返回空对象
  const studentScoreList = maxExam ?
    [maxExam["0-30分段学生数量"],
    maxExam["30-60分段学生数量"],
    maxExam["60-90分段学生数量"],
    maxExam["90-120分段学生数量"],
    maxExam["120-150分段学生数量"],
    ] : []
  data2.value = [studentScoreDistribution, studentScoreList]
  return [studentScoreDistribution, studentScoreList]
};
const getData3 = () => {

};
const getData4 = () => {

};

// 弹幕数据和颜色
const danmus = ref<string[]>([
  '今天天气不错，适合出去散步。',
  '明天有个重要的会议，需要准备一下。',
  '中午吃什么好呢？我想吃火锅。',
  '这个周末打算去旅游，还没定好目的地。',
  '最近在学习一门新的技术，挺有意思的。',
  '生活总是充满了各种各样的惊喜。',
  '时间过得真快，转眼间又到了周末。',
  '每天都要保持好心情，生活才会更美好。'
]);

const colors = ref<string[]>([
  "#ffb980", "#2ec7c9", "#5ab1ef", "#b6a2de", "#d87a80",
  "#8d98b3", "#e5cf0d", "#97b552", "#95706d", "#dc69aa",
  "#07a2a4", "#9a7fd1", "#588dd5", "#f5994e", "#c05050",
  "#59678c", "#c9ab00", "#7eb00a", "#6f5553", "#c14089",
  "#409eff",
]);
</script>

<style lang="less" scoped>
.baberrage {
  width: 100%;
  height: 400px;
  background: #ffffff;

  .danmaku {
    width: 100%;
    height: 100%;

    &-name {}
  }
}

.carousel {
  display: block;
  text-align: center;
  width: 100%;
  height: 400px;

}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
