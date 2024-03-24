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
              <Result v-if="state.LLMData" 
              :LLMData="state.LLMData" 
              @updateValue="handleUpdateValue($event)"
              />
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
import { ElMessageBox, ElLoading } from 'element-plus';
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

  methods: {
    handleUpdateValue(newValue) {
      this.state.LLMData = newValue;  // 更新相应的值
    }
  },
  setup(props){
    
    const axios = inject('axios') as AxiosInstance
    const state = reactive({  //  Vue 的响应性 API，当我们改变这个数据时，Vue 能知道需要重新渲染影响的组件。
      currentPage: 0,
      currentSet: 0,
      imageSources:[],
      paper_id:0,
      LLMData:null,
      original_data:null,
    });
    state.paper_id=props.paper_id
    console.log("TopBar props.paperData:", props.paperData)
    const fetchImageFromServer = () => {
      const loading = ElLoading.service({
          lock: true,
          text: '加载中',
          background: 'rgba(0, 0, 0, 0.7)',
      })

      const response = axios.get(`exams/querypaper/${state.paper_id}/`)
        .then(response => {
          state.imageSources = response.data.map(img_base64 => 'data:image/jpg;base64,' + img_base64);
          loading.close()
        }).catch(function (error) {
                      console.log(error);
                      loading.close()
                      ElMessageBox.alert('加载失败!', '警告', {
                        confirmButtonText: '确定'
                      })
                    });
      
    };

    // const getAllValues = (obj) => {
    //   let result = [];

    //   for (let i in obj) {
    //     //console.log(i)
    //     if (!isNaN(Number(i)) && parseInt(Number(i)) == Number(i)) {
    //       let tmp=obj[i]
    //       obj[i].index=Number(i)
    //       result.push(obj[i]);
    //     } else {
    //       result = result.concat(getAllValues(obj[i]));
    //     }
    //   }
    //   return result;
    // }

    const getAllValues = (curindex, obj) => {
      let result = [];

      for (let i in obj) {
        if ((obj[i] instanceof Object )) { //如果当前元素是字典，并且子元素不是字典，说明这个题没有子题
          for ( let j in obj[i]){
            if (!(obj[i][j]  instanceof Object)){
              obj[i].index=curindex+' '+i
              //console.log(obj[i])
              //console.log('obj[i][j]:',obj[i][j])
              result.push(obj[i]);  //
              break
            }else{
              result = result.concat(getAllValues(curindex+' '+i,obj[i]).result); //如果当前题目还是子题，继续遍历
              break
            }
          }
        } else {
          result = result.concat(getAllValues(curindex, obj[i]).result);
        }
      }
      return {
        'curindex':curindex,
        'result':result};
    }


    const getLLMPreprocess = async () => {
      console.log('get LLM Preprocess');
      try {

        const response = await axios.get(`exams/queryllm/${state.paper_id}/`);
        let response_data=response.data
        state.original_data=response_data
        console.log('response_data:',response_data)
        let result=getAllValues('',response_data).result
        console.log('转换得到的data：',result)
        state.LLMData=result
        console.log("TopBar LLM Marking Paper Response.data:",state.LLMData);
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

    const Update = (parts, idx,obj, org) => {
      while(parts[idx]==''){
        idx+=1
      }
      console.log('%%%%%%%%%%',org, parts[idx],idx)
      if (parts.length-1==idx){
        org[parts[idx]]=obj
        return org;
      }
      Update(parts, idx+1, obj, org[parts[idx]])
      
    }

    const nextOne = async () => {
      try {

        for (let i in state.LLMData){
          let obj=state.LLMData[i]
          console.log(obj.index, obj)
          let parts=obj.index.split(" ")

          console.log('parts:', parts)
          Update(parts,0, obj, state.original_data)
        }

        const response =await axios.post(`exams/marking_update/${state.paper_id}/`,state.original_data)
        console.log(response);
        await ElMessageBox.alert('当前批改内容已经保存！', '提示', {
        confirmButtonText: '确定'
     })
      }catch (error) {
        console.log(error);
        await ElMessageBox.alert('当前批改内容保存失败！', '警告', {
          confirmButtonText: '确定'
        })
      }
      
      if (state.currentSet+1===props.totalSet){
        nextTick(() => {
          ElMessageBox.alert('你已经在最后一份了!', '提示', {
            confirmButtonText: '确定'
          })
        });
      }else{
        state.currentSet+=1
        console.log("下一份:",state.currentSet )
        console.log("下一份:",props.paperData[state.currentSet] )
        state.currentPage=0
        state.paper_id=props.paperData[state.currentSet].paper_id
        
        fetchImageFromServer();
      }
      
    };

    const prevOne = () => {
      if (state.currentSet===0){
        nextTick(() => {
          ElMessageBox.alert('你已经在第一份了!', '提示', {
            confirmButtonText: '确定'
          })
        });
      }else{
        state.currentSet-=1
        console.log("上一份:",state.currentSet )
        console.log("上一份:",props.paperData[state.currentSet] )
        state.currentPage=0
        state.paper_id=props.paperData[state.currentSet].paper_id

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
