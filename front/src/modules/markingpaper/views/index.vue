<template>
  <Topbar />
</template>

<script lang="ts">
import { defineComponent, onMounted, inject, reactive } from 'vue'
import { useRoute } from 'vue-router';
import { AxiosInstance } from 'axios';
import Topbar from './components/Topbar.vue'

export default defineComponent({
  name: 'MarkingPaper',
  components:{
    Topbar,
  },
  data() {
    return {
    };
  },
  setup() {
    const route = useRoute()
    // 获取 exam_id
    const axios = inject('axios') as AxiosInstance
    const paper_id = route.query.paper_id
    console.log('批改试卷 paper_id:',paper_id)

    const state = reactive({  //  Vue 的响应性 API，当我们改变这个数据时，Vue 能知道需要重新渲染影响的组件。
      paperImg:[],
      msg:0,
    })

    // const fetchFiles = async () => {
    //   const response = await axios({
    //     url: `exams/querypaper/${paper_id}/`,  // Django端点URL，你需要更改为你自己的端点
    //     method: 'GET',
    //     responseType: 'blob',
    //   });
      
    //   const url = window.URL.createObjectURL(new Blob([response.data]));
    //   const link = document.createElement('a');
    //   link.href = url;
    //   link.setAttribute('download', 'my_files.zip');
    //   document.body.appendChild(link);
    //   link.click();

    // }


    onMounted(async() => {
      try {
        const response = await axios.get(`exams/querypaper/${paper_id}/`, {responseType:'blob'});
        //const response = await axios.get('exams/test/');
        state.msg = response.data;
        console.log('state.msg:',state.msg)
        
      }catch(e) {
        console.log('Paper Error:', e)
      }  
    });
  },
  
  // methods: {
  //   fetchFiles() {
  //     const axios = inject('axios') as AxiosInstance
  //     axios({
  //       url: '/download_files/',  // Django端点URL，你需要更改为你自己的端点
  //       method: 'GET',
  //       responseType: 'blob', 
  //     }).then((response) => {
  //       const url = window.URL.createObjectURL(new Blob([response.data]));
  //       const link = document.createElement('a');
  //       link.href = url;
  //       link.setAttribute('download', 'my_files.zip');
  //       document.body.appendChild(link);
  //       link.click();
  //     });
  //   }
  // },
  
})
</script>
