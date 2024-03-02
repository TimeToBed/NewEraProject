<template>
  <div class="w-full block mx-auto h-auto py-2">
    <div class="flex-wrap flex-col bg-white shadow mb-7 mx-auto rounded-md">
      <div class="flex py-5 px-6 border-b border-primary-white">
        <h3 class="cursor-auto">创建考试</h3>
        <ul class="flex list-none justify-around flex-grow">
          <li>基本信息</li>
          <li>上传试卷</li>
          <li>完成</li>
        </ul>
      </div>
      
      <div class="p-4 items-center justify-center h-full">
        <div class="w-full py-10 flex items-center justify-center">

          <BasicInfo 
            :exam-info="examInfo"
            v-if="currentStep === 1" @continue="nextStep" />
          <UploadPaper
            :exam-info="examInfo"
             v-else-if="currentStep === 2" @continue="nextStep" @back="previousStep" />
          <Finish 
            :exam-info="examInfo"
            v-else-if="currentStep === 3" @back="previousStep" @submit="submitExam" />
          
        </div> 
      </div>
    </div>
    
  </div>
</template>

<script lang="ts">
import { defineComponent, inject, reactive, ref } from 'vue'
import BasicInfo from './BasicInfo.vue'
import UploadPaper from './UploadPaper.vue'
import Finish from './Finish.vue'
import { AxiosInstance } from 'axios'

export default defineComponent({
  name: 'Topbar',
  components: {
    BasicInfo,
    UploadPaper,
    Finish
  },

  setup(){
    const examInfo = reactive({
      examname: '',
      subject: '',
      time: '',
      paper: Object,
      result: Object,
      teacher_id: 1
    })
    // 从全局中获取 axios
    const axios = inject('axios') as AxiosInstance

    const currentStep = ref(1);
    const submitExam = async () => {
      console.log(typeof(examInfo.paper));
      console.log('提交考试');
      // 通过axios发送一个POST请求到您的后端
      const response = await axios.post('exams/create_exam/', examInfo);
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
      examInfo, currentStep, submitExam, nextStep, previousStep
    }
  }

})
</script>
