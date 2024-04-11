<template>
  <div class="w-full mx-auto">
    <div class="w-full">
      <AnalysisCard :Datalist="data1" />
    </div>

    <div class="mt-6">
      <div class="flex flex-wrap">
        <div class="lg:flex-8 lg:max-w-2/3 w-full lg:mb-0 lg:pr-3.5 mb-6">
          <GradientLineChart :Datalist="data3" />
        </div>
        <div class="lg:flex-4 lg:max-w-1/3 w-full lg:pl-3.5">
          <TotalBarChart :Datalist="data2" />
        </div>
      </div>
    </div>

    <div class="mt-6">
      <div class="flex flex-wrap">
        <div class="lg:flex-8 lg:max-w-2/3 w-full lg:mb-0 lg:pr-3.5" style="height: 250;">
          <PageVisitTable :Datalist="data4" />
          <!-- <el-table :data="data4.value" style="width: 100%">
            <el-table-column prop="name" label="姓名" />
            <el-table-column prop="score" label="分数" />
            <el-table-column prop="rank" label="排名" />
          </el-table> -->
        </div>
        <div class="lg:flex-4 lg:max-w-1/3 w-full lg:pl-3.5">
          <SocialTrafficTable :Datalist="data5" />
        </div>
      </div>
    </div>
    <div class="mt-6">
      <div class="flex flex-wrap">
        <div class="lg:flex-8 lg:max-w-2/3 w-full lg:mb-0 lg:pr-3.5">
          <div class="carousel">
            <el-carousel height="400px">
              <el-carousel-item v-for="item in danmus.value" :key="item">
                <h3 class="carousel-text" text="2xl"
                  :style="[{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }, { color: colors[Math.round(Math.random() * 20)] }]">
                  {{ item }}</h3>
              </el-carousel-item>
            </el-carousel>
          </div>
        </div>
        <div class="lg:flex-4 lg:max-w-1/3 w-full lg:pl-3.5">
          <div class="baberrage">
            <vue-danmaku class="danmaku" ref="danmakuRef" v-model:danmus="danmus.value" useSlot loop :speeds="100" :top="50"
              :right="50" :fontSize="50" :randomChannel=true>
              <template v-slot:dm="{ danmu }">
                <div :style="{ color: colors[Math.round(Math.random() * 20)] }">{{ danmu }}</div>
              </template>
            </vue-danmaku>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { ref, inject, onMounted, computed, defineComponent, reactive } from 'vue'
import { AxiosInstance } from 'axios'
import vueDanmaku from 'vue3-danmaku'
// import type { TableInstance } from 'element-plus'
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
export default defineComponent({
  name: 'Dashboard',
  components: {
    AnalysisCard,
    GradientLineChart,
    TotalBarChart,
    SocialTrafficTable,
    PageVisitTable,
    vueDanmaku
  },
  setup() {
    // 使用axios进行数据获取
    const axios = inject('axios') as AxiosInstance | undefined;
    // 数据
    const dataList = ref({});
    const data1 = ref<number[]>([]);
    const data2 = ref({});
    const data3 = ref({});
    const data4 = reactive({});
    const data5 = reactive({});
    // 弹幕数据和颜色
    const danmus = reactive({});

    const colors = ref<string[]>([
      "#ffb980", "#2ec7c9", "#5ab1ef", "#b6a2de", "#d87a80",
      "#8d98b3", "#e5cf0d", "#97b552", "#95706d", "#dc69aa",
      "#07a2a4", "#9a7fd1", "#588dd5", "#f5994e", "#c05050",
      "#59678c", "#c9ab00", "#7eb00a", "#6f5553", "#c14089",
      "#409eff",
    ]);
    // 定义获取数据的异步函数
    async function getDataList() {
      if (!axios) {
        console.error("Axios instance not found");
        return;
      }

      try {
        const response = await axios.get(`exams/data_list/2/`);
        getData1(response.data);
        getData2(response.data);
        getData3(response.data);
        getData4(response.data);
        getData5(response.data);
        dataList.value = response.data; // 将获取的数据存储到响应式引用中
      } catch (error) {
        console.error("Error during HTTP request:", error);
      }
    }
    // 获取轮播图内容
    async function getCarouselData() {
      if (!axios) {
        console.error("Axios instance not found");
        return;
      }
      try {
        const response = await axios.post(`exams/comment/`);
        console.log(response)
        danmus.value = response.data.comments
      }
      catch (error) {
        console.error("Error during HTTP request:", error);
      }
    }
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
      // const maxKey = Math.min(...Object.keys(student_count)
      //   .filter(key => /^\d+$/.test(key)) // 筛选出纯数字的键
      //   .map(Number)); // 转换为数字
      // step2 获取最近一次考试
      const maxExam = Object.values(e.data_dict)[0];
      // const maxExam = student_count[0];
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
    function getData3(e: DataStructure): { examName: string; averageScore: number; }[] {
      const re = Object.entries(e.data_dict)
        .filter(([_, examDetails]) => examDetails.hasOwnProperty('平均成绩') && typeof examDetails['平均成绩'] === 'number')
        .map(([examName, examDetails]) => ({
          examName,
          averageScore: examDetails['平均成绩']
        }));

      // 提取 labels 和 data
      const labels = re.map(result => result.examName);
      const data = re.map(result => result.averageScore);
      data3.value = [labels, data]
    }
    function getData4(e: DataStructure) {
      const maxExam = e.student_dict;
      console.log(maxExam)
      if (!maxExam || !maxExam["进步人数占比"]) {
        console.error('Max exam or its scores are missing.');
        return [];
      }

      // const studentScores = maxExam;

      // // 处理成绩并分配排名
      // const scoresArray = Object.entries(studentScores).map(([studentId, score]) => ({
      //   studentId,
      //   score: score !== "-" ? parseInt(score as string, 10) : null,
      // })).sort((a, b) => b.score - a.score || parseInt(a.studentId) - parseInt(b.studentId));

      // const results = scoresArray.map((item, index, array) => ({
      //   name: `${item.studentId}`,
      //   score: item.score !== null ? `${item.score}` : "-",
      //   rank: (index > 0 && item.score === array[index - 1].score) ? array[index - 1].userNumber : index + 1,
      //   rate: 0, // Placeholder for 'rate', as it's unspecified how to calculate it
      // }));
      // 从student_dict中提取学生成绩，排除“进步人数占比”
      // 从student_dict中提取学生成绩，排除“进步人数占比”
      const studentDetails = Object.entries(e.student_dict).reduce((acc, [studentId, details]) => {
        // 排除“进步人数占比”
        if (studentId !== "进步人数占比") {
          acc.push({
            name: studentId,
            score: details["最近一次考试成绩"],
            rate: details["上升幅度"]
          });
        }
        return acc;
      }, []);

      // 将学生成绩排序（高分在前）
      studentDetails.sort((a, b) => b.score - a.score);

      // 分配排名
      const results = studentDetails.map((item, index, array) => ({
        ...item,
        rank: index + 1, // 直接使用索引加1作为排名
      }));

      data4.value = results
      return results;
    }
    function getData5(e: DataStructure) {
      // 获取最近一次考试的详细信息
      let latestExamDetails = Object.values(e.data_dict)[0];
      // 用于存储所有考试的得分率信息
      let allExamsScoreRates = [];

      // 遍历所有考试
      // Object.entries(maxExam).forEach(([examName, examDetails]) => {
      //   // 检查考试对象是否有效
      //   if (examDetails && typeof examDetails === 'object') {
      //     // 遍历考试详情中的每个字段
      //     Object.entries(examDetails).forEach(([key, value]) => {
      //       // 如果键名包含“得分率”，则将其格式化后添加到结果数组中
      //       if (key.includes("得分率")) {
      //         allExamsScoreRates.push({
      //           name: key,
      //           score: value
      //         });
      //       }
      //     });
      //   }
      // });
      // 检查最近一次考试对象是否有效
      if (latestExamDetails && typeof latestExamDetails === 'object') {
        // 遍历最近一次考试详情中的每个字段
        Object.entries(latestExamDetails).forEach(([key, value]) => {
          // 如果键名包含“得分率”，则将其格式化后添加到结果数组中
          if (key.includes("得分率")) {
            allExamsScoreRates.push({
              name: key,
              score: value
            });
          }
        });
      }

      // 打印所有考试的得分率信息，以便检查
      console.log(allExamsScoreRates);

      // 更新响应式数据
      data5.value = allExamsScoreRates;
      return allExamsScoreRates;
    }

    // 使用onMounted生命周期钩子在组件挂载时调用getDataList
    onMounted(() => {
      getDataList();
      getCarouselData();
    });
    return {
      dataList,
      data1,
      data2,
      data3,
      data4,
      data5,
      danmus,
      colors
    }
  }
})

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

.el-carousel__item:nth-child(n) {
  background-color: #ffffff;
  box-shadow: inset 0 0 39px #53a8ff;
}
</style>