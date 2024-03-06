<template>
  <div class="w-full block mx-auto h-auto py-2">
    <div class="flex-wrap flex-col bg-white shadow mb-7 mx-auto rounded-md">
      <div class="flex justify-between py-5 px-6 border-b border-primary-white">
        <h3 class="cursor-auto">批改试卷</h3>
        <div class="flex space-x-4">
          <p>当前份数: {{ currentSet }}/{{ currentSet }}</p>
          <p>当前页数：{{ currentPage }}/{{ totalPage }}</p>
          <button @click="nextOne">下一份</button>
          <button @click="exit">退出</button>
        </div>
      </div>
      
      <div class="p-4 items-center justify-center h-full">
        <div class="mt-1">
          <div class="flex flex-wrap">
            <div class="lg:flex-8 lg:max-w-2/3 w-full lg:mb-0 lg:pr-3.5 mb-6">
              <Paper />
            </div>
            <div class="lg:flex-4 lg:max-w-1/3 w-full lg:pl-3.5">
              <Result />
            </div>
          </div>
        </div>
      </div>
      
      <div class="flex justify-between py-5 px-6 border-b border-primary-white">
        <div class="flex justify-end">
            <el-button type="success" @click="nextForm">下一页</el-button>
        </div>
      </div>

    </div>
    
  </div>
</template>

<script lang="ts">
import { defineComponent, inject, reactive, ref } from 'vue'
import Paper from './Paper.vue'
import Result from './Result.vue'
import { AxiosInstance } from 'axios'

export default defineComponent({
  name: 'Topbar',
  components: {
    Paper,
    Result,
  },
  created() {
    console.log('received id is: ', this.$route.query.paper_id);
  },
  methods: {
    nextOne() {
      console.log("Handle the click on the 下一份 button")
    },
    exit() {
      console.log("Handle the click on the 退出 button")
    }
  },
  setup(){
    const examInfo = reactive({
      examname: '',
      subject: '',
      time: '',
      paper: null,
      result: null,
      teacher_id: 1
    })
    // 从全局中获取 axios
    const axios = inject('axios') as AxiosInstance

    const currentSet=1
    const totalSet=40
    const currentPage=1
    const totalPage=4

    const currentStep = ref(1);
    const submitExam = async () => {

      console.log(typeof(examInfo.paper));
      console.log('提交考试');
      let formData = new FormData();

      // Append the other parts of examInfo
      formData.append('examname', examInfo.examname);
      formData.append('subject', examInfo.subject);
      formData.append('time', examInfo.time);
      formData.append('teacher_id', examInfo.teacher_id.toString());

      // Append the files
      if(examInfo.paper){
        console.log(examInfo.paper);
        formData.append('paper', examInfo.paper['raw']);
      }
      if(examInfo.result){
        formData.append('result', examInfo.result['raw']);
      }
      
      // 通过axios发送一个POST请求到您的后端
      const response = await axios.post('exams/create_exam/', formData);
      console.log(response.data);
    }

    const nextStep = () => {
      currentStep.value += 1;
      console.log('currentStep:', currentStep.value)
    }

    const previousStep = () => {
      currentStep.value -= 1;
      console.log('currentStep:', currentStep.value)
    }

    

    return {
      examInfo, currentStep, submitExam, nextStep, previousStep,
      currentSet, totalSet, currentPage, totalPage,
    }
  }

})
</script>
