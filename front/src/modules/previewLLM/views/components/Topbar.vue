<template>
  
  <div class="w-full block mx-auto h-auto py-2">
    <div class="flex-wrap flex-col bg-white shadow mb-7 mx-auto rounded-md">
      <div class="flex justify-between py-2 px-6 border-b border-primary-white">
        <h3 class="cursor-auto">大模型分析结果</h3>
      </div>
      
      <div class="p-4 items-center justify-center h-full">
        <div class="mt-1">
          <div class="flex flex-wrap">
            <div class="lg:flex-8 lg:max-w-2/3 w-full lg:mb-0 lg:pr-3.5 mb-6">
              <Paper 
              class="h-600"
              v-if="state.fileSources"
               :file_src="state.fileSources"/>
               <Paper 
                class="h-600"
                v-if="!state.fileSources"
                />
            </div>
            <div class="lg:flex-4 lg:max-w-1/3 w-full lg:pl-3.5">
              <Result 
                v-if="state.LLMData" :LLMData="state.LLMData" 
                :key="state.componentKey"
                @updateValue="handleUpdateValue($event)"
                />
            </div>
          </div>
        </div>
      </div>

      <div class="flex py-2 px-6 border-b border-primary-white">
        <!-- <div class="flex justify-end ml-5">
            <el-button type="success" @click="prevPage">上一页</el-button>
        </div>
        <div class="flex justify-end ml-5">
            <el-button type="success" @click="nextPage">下一页</el-button>
        </div> -->
        
        <div class="flex justify-end ml-5">
          <el-button type="success" style="height: 2rem;"  @click="ok">确认</el-button>
        </div>

        
        <div class="flex justify-end ml-5">
          <el-button type="success" style="height: 2rem;"  @click="reset">重置</el-button>
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

export default defineComponent({
  name: 'Topbar',
  components: {
    Paper,
    Result,
  },
  props:{
    exam_id:{
        type: Number,
        required: true,
      },
  },
  methods: {
    handleUpdateValue(newValue) {
      this.state.LLMData = newValue;  // 更新相应的值
    }
  },
  setup(props){
    
    const axios = inject('axios') as AxiosInstance
    const state = reactive({  //  Vue 的响应性 API，当我们改变这个数据时，Vue 能知道需要重新渲染影响的组件。
      exam_id:0,
      imageSources:[],
      LLMData:null,
      currentPage:0,
      totalPage:0,
      componentKey:0,
      fileSources:null,
    });
    state.exam_id=props.exam_id
    const fetchPaperFromServer = () => {
      axios({
        method: "get",
        responseType: "blob", // 因为是流文件，所以要指定blob类型
        url:`llms/llm_preview/${state.exam_id}/`,
      }).then(({ data }) => {
        console.log('data:',data); // 后端返回的是流文件
        state.fileSources=data
      });
    };
    const getLLMPreprocess = async () => {
      console.log('get LLM Preprocess');
      try {
        const response = await axios.get(`llms/llm_preprocess/${state.exam_id}/`);
        state.LLMData=response.data
        console.log("TopBar LLM Preprocess Response.data:",state.LLMData);
      } catch (error) {
        console.error("Error during HTTP request:", error);
      }
    }

    getLLMPreprocess()
    fetchPaperFromServer()
    const nextPage = () => {
      if (state.currentPage+1===props.totalPage){
        nextTick(() => {
          ElMessageBox.alert('你已经在最后一页了!', '提示', {
            confirmButtonText: '确定'
          })
        });
      }else{
        state.currentPage+=1
        console.log('下一页------------------')
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


    const ok = () => {
      console.log("确认")
      const response = axios.post(`llms/llm_update/${state.exam_id}/`,state.LLMData
                                  )
                        .then(function (response) {
                          console.log(response);
                          ElMessageBox.alert('您的修改已经保存！', '提示', {
                                confirmButtonText: '确定'
                              })
                        })
                        .catch(function (error) {
                          console.log(error);
                        });
      
    };
    
    const reset = () => {
      console.log("重置")
      //getLLMPreprocess()
      state.componentKey+=1
    };

    return {
      state,
      nextPage,
      prevPage,
      fetchPaperFromServer,
      getLLMPreprocess,
      ok,
      reset,
    }
  }
})
</script>
