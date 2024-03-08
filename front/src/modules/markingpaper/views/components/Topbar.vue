<template>
  
  <div class="w-full block mx-auto h-auto py-2">
    <div class="flex-wrap flex-col bg-white shadow mb-7 mx-auto rounded-md">
      <div class="flex justify-between py-5 px-6 border-b border-primary-white">
        <h3 class="cursor-auto">批改试卷</h3>
        <div class="flex space-x-4">
          <p>当前份数: {{ state.currentSet+1 }}/{{ totalSet }}</p>
          <p>当前页数：{{ state.currentPage+1 }}/{{ totalPage }}</p>
          <button @click="prevOne">上一份</button>
          <button @click="nextOne">下一份</button>
          <button @click="exit">退出</button>
        </div>
      </div>
      
      <div class="p-4 items-center justify-center h-full">
        <div class="mt-1">
          <div class="flex flex-wrap">
            <div class="lg:flex-8 lg:max-w-2/3 w-full lg:mb-0 lg:pr-3.5 mb-6">
              <Paper :img_src="state.imageSources[state.currentPage]"/>
            </div>
            <div class="lg:flex-4 lg:max-w-1/3 w-full lg:pl-3.5">
              <Result v-if="state.LLMData" :LLMData="state.LLMData" />
            </div>
          </div>
        </div>
      </div>

      <div class="flex py-5 px-6 border-b border-primary-white">
        <div class="flex justify-end ml-5">
            <el-button type="success" @click="prevPage">上一页</el-button>
        </div>
        <div class="flex justify-end ml-5">
            <el-button type="success" @click="nextPage">下一页</el-button>
        </div>
      </div>

    </div>
    
  </div>
</template>

<script lang="ts">
import { defineComponent, inject, reactive, ref ,nextTick} from 'vue'
import Paper from './Paper.vue'
import Result from './Result.vue'
import { AxiosInstance } from 'axios'
import { ElMessageBox } from 'element-plus';
import PaperData from 'modules/paperlist/views/components/PaperData.vue';
import { stat } from 'fs';

export default defineComponent({
  name: 'Topbar',
  components: {
    Paper,
    Result,
  },
  props:{
    paper_id:{
        type: Number,
        required: true,
      },
    totalSet:{
        type: Number,
        required: true,
      },
    totalPage:{
        type: Number,
        required: true,
      },
    paperData:{
        type: Array,
        required: true,
      },
  },

  setup(props){
    
    const axios = inject('axios') as AxiosInstance
    const state = reactive({  //  Vue 的响应性 API，当我们改变这个数据时，Vue 能知道需要重新渲染影响的组件。
      currentPage: 0,
      currentSet: 0,
      imageSources:[],
      paper_id:0,
      LLMData:null
    });
    state.paper_id=props.paper_id

   const fetchImageFromServer = () => {
      axios.get(`exams/querypaper/${state.paper_id}/`)
        .then(response => {
          state.imageSources = response.data.map(img_base64 => 'data:image/jpg;base64,' + img_base64);
      });
    };

    const getLLMPreprocess = async () => {
      console.log('get LLM Preprocess');
      try {
      
        const response = await axios.get(`exams/llm_preprocess/${state.paper_id}/`);
        state.LLMData=response.data
        console.log("TopBar LLM Preprocess Response.data:",state.LLMData);
      } catch (error) {
        console.error("Error during HTTP request:", error);
      }
    }

    getLLMPreprocess()
    fetchImageFromServer()
    const nextPage = () => {
      if (state.currentPage+1===props.totalPage){
        nextTick(() => {
          ElMessageBox.alert('你已经在最后一页了!', '提示', {
            confirmButtonText: '确定'
          })
        });
      }else{
        state.currentPage+=1
      }
    };

    const prevPage = () => {
      if (state.currentPage===0){
        nextTick(() => {
          ElMessageBox.alert('你已经在第一页了!', '提示', {
            confirmButtonText: '确定'
          })
        });
      }else{
        state.currentPage-=1
      }
      
    };

    const nextOne = () => {
      if (state.currentSet+1===props.totalSet){
        nextTick(() => {
          ElMessageBox.alert('你已经在最后一份了!', '提示', {
            confirmButtonText: '确定'
          })
        });
      }else{
        const axios = inject('axios') as AxiosInstance
        state.currentSet+=1
        console.log("下一份:",state.currentSet )
        console.log("下一份:",props.paperData[state.currentSet] )
        state.currentPage=0
        state.paper_id=props.paperData[state.currentSet].paper_id
        //const response = axios.get(`exams/next_paper/${state.paper_id}/`);
        
        fetchImageFromServer();
      }
      
    };

    const prevOne = () => {
      if (state.currentSet+1===0){
        nextTick(() => {
          ElMessageBox.alert('你已经在第一份了!', '提示', {
            confirmButtonText: '确定'
          })
        });
      }else{
        console.log("上一份")
        state.currentSet-=1
        state.currentPage=0
        fetchImageFromServer();
      }
      
    };

    return {
      state,
      nextPage,
      prevPage,
      nextOne,
      prevOne,
      fetchImageFromServer,
      getLLMPreprocess
    }
  }
})
</script>
