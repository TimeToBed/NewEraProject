<template>
  <div class="w-full block mx-auto h-auto py-2">
    <div class="flex flex-wrap flex-col bg-white shadow mb-7 mx-auto rounded-md">
      <div class="py-5 px-6 border-b border-primary-white">
        <h3 class="cursor-auto">考 试 列 表</h3>
      </div>
      <div class="block overflow-x-auto w-full">
        <ExamData :tableData="state.exam" />
      </div>
      <!-- <div class="p-4">
        <Pagination />
      </div> -->
    </div>
    
  </div>
</template>

<script lang="ts">
import { AxiosInstance } from 'axios'
import { defineComponent, inject, reactive, onMounted } from 'vue'
import ExamData from './components/ExamData.vue'


interface User {
  avatarPath: string
  name: string
}
interface Exam {
  exam_id: number,
  exam_name: string,
  exam_date: string,
  subject: string,
  markingable: boolean
}

export default defineComponent({
  name: 'ExamList',
  components: {
    ExamData,
  },
  
  setup(){
    const axios = inject('axios') as AxiosInstance
    const state = reactive({  //  Vue 的响应性 API，当我们改变这个数据时，Vue 能知道需要重新渲染影响的组件。
      exam: null
    })
     
    onMounted(async() => {
      try {
        const user_id= '1'
        const response = await axios.get(`exams/examlist/${user_id}/`);
        //const response = await axios.get('exams/test/');
        state.exam = response.data;
        console.log('state.exam:',state.exam)
        console.log('response.data:', response.data)
      }catch(e) {
        console.log('Exam Error:', e)
      }   
    });
    return {
      state
    }
  }
})
</script>
  