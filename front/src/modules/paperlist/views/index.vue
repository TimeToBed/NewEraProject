<template>
  <div class="w-full block mx-auto h-auto py-2">
    <div class="flex flex-wrap flex-col bg-white shadow mb-7 mx-auto rounded-md">
      <div class="py-5 px-6 border-b border-primary-white">
        <h3 class="cursor-auto">试 卷 列 表</h3>
      </div>
      <div class="block overflow-x-auto w-full">
        <PaperData :tableData="state.paper" />
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
import { useRoute } from 'vue-router'
import PaperData from './components/PaperData.vue'


interface User {
  avatarPath: string
  name: string
}
interface Paper {
  paper_id: number,
  state: number,
  pages: number,
  student_id: string,
  student_name: string,
}

export default defineComponent({
  name: 'PaperList',
  components: {
    PaperData,
  },
  created() {
    console.log('received id is: ', this.$route.query.exam_id);
  },
  setup(){
    const axios = inject('axios') as AxiosInstance
    const state = reactive({  //  Vue 的响应性 API，当我们改变这个数据时，Vue 能知道需要重新渲染影响的组件。
      paper: null
    })
     
    onMounted(async() => {
      try {
        const route = useRoute();
        const exam_id= route.query.exam_id
        const response = await axios.get(`/exams/paperlist/${exam_id}/`);
        // //const response = await axios.get('exams/test/');
        state.paper = response.data;
        console.log('state.paper:',state.paper)
        console.log('response.data:', response.data)

      }catch(e) {
        console.log('Paper Error:', e)
      }   
    });
    return {
      state
    }
  }
})
</script>
  