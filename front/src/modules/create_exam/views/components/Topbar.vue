<template>
  <div class="w-full block mx-auto h-auto py-2">
    <div class="flex-wrap flex-col bg-white shadow mb-7 mx-auto rounded-md">
      <div class="flex py-5 px-6 border-b border-primary-white">
        <h3 class="cursor-auto">创建考试</h3>
        <ul class="flex list-none justify-around flex-grow ">
          <li class="flex items-center justify-center">
            <PencilAltIcon v-if="currentStep === 1" 
              class="h-5 w-5 text-indigo-410" />
            <CheckIcon v-else 
              class="h-5 w-5 text-indigo-410" />
            <p class="text-indigo-410"
              :class="{'font-bold': currentStep === 1}">基本信息</p>
          </li>
          <li class="flex items-center justify-center">
            <PencilAltIcon v-if="currentStep === 2" class="h-5 w-5 text-indigo-410"/>
            <CheckIcon v-else-if="currentStep === 3 || currentStep === 4" class="h-5 w-5 text-indigo-410" />
            <PencilAltIcon v-else class="h-5 w-5"/>
            <p class="text-indigo-410"
              :class="{'font-bold': currentStep === 2,
                'text-dark': currentStep === 1}">上传试卷</p>
          </li>
          <li class="flex items-center justify-center">
            <PencilAltIcon v-if="currentStep === 3" class="h-5 w-5 text-indigo-410"/>
            <CheckIcon v-else-if="currentStep === 4" class="h-5 w-5 text-indigo-410" />
            <PencilAltIcon v-else class="h-5 w-5"/>
            <p 
              :class="{'font-bold text-indigo-410': currentStep === 3 || currentStep === 4}">完成</p>
          </li>
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
            :currentStep="currentStep" 
            v-else-if="currentStep === 3 || currentStep === 4" 
            @continue="nextStep" @back="previousStep" @submit="submitExam" 
            @reset-currentStep="updataCurrentStep"
            @reset-exam-info="resetExamInfo"/>
          
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
import {PencilAltIcon, CheckIcon } from '@heroicons/vue/solid'


export default defineComponent({
  name: 'Topbar',
  components: {
    BasicInfo,
    UploadPaper,
    Finish,
    PencilAltIcon,
    CheckIcon,
  },

  setup(){
    const initialExamInfo = {
      exam_id: 1,
      examname: '',
      subject: '',
      time: '',
      paper: null,
      result: null,
      teacher_id: 1
    }
    const examInfo = reactive({...initialExamInfo})
    // 从全局中获取 axios
    const axios = inject('axios') as AxiosInstance

    const currentStep = ref(1);
    const submitExam = async () => {
      let formData = new FormData();

      // Append the other parts of examInfo
      formData.append('examname', examInfo.examname);
      formData.append('subject', examInfo.subject);
      formData.append('time', examInfo.time);
      let teacher_id=localStorage.getItem('user_id')
      formData.append('teacher_id', teacher_id);

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
      examInfo.exam_id = response.data.exam_id;
      console.log(response.data);
      console.log(examInfo.exam_id);
    }

    const nextStep = () => {
      currentStep.value += 1;
      console.log('currentStep:', currentStep.value)
    }

    const previousStep = () => {
      currentStep.value -= 1;
      if(currentStep.value < 1){
        currentStep.value = 1;
      }
      console.log('currentStep:', currentStep.value)
    }

    const updataCurrentStep = (newValue: number) => {
      currentStep.value = newValue;
    }

    const resetExamInfo = () => {
      Object.assign(examInfo, initialExamInfo)
    }

    return {
      examInfo, currentStep, submitExam, nextStep, previousStep, PencilAltIcon, CheckIcon, 
      updataCurrentStep, resetExamInfo
    }
  }

})
</script>
