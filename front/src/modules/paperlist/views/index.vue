<template>
  <div class="w-full block mx-auto h-auto py-2">
    <div class="flex flex-wrap flex-col bg-white shadow mb-7 mx-auto rounded-md">
      <ul class="py-5 px-6 border-b border-primary-white flex list-none justify-between flex-grow">

        <li><h3 class="cursor-auto">试 卷 列 表</h3></li>
        <li>
          <el-button  
          
          type="primary"  size="samll" @click="handleButtonClickOCRPreprocess()">
            预处理
          </el-button>
        </li>
      </ul>
      <div class="block overflow-x-auto w-full">
        <PaperData 
        :tableData="state.paper" 
        :totalSet="state.Total"
        />
      </div>
      <div class="p-4">
        <div class="w-full">
          <div class="flex justify-end mb-0">
            <el-pagination
              @size-change="handlehSizeChange"
              @current-change="handlehCurrentChange"
              :current-page="state.CurrentPage"
              :page-sizes="[10, 20, 30, 40]"
              :page-size="state.PageSize"
              layout="total, jumper , prev, pager, next, sizes"
              :total="state.Total"
              popper-class="label-popper"
            >
            </el-pagination>
          </div>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script lang="ts">
import { AxiosInstance } from 'axios'
import { defineComponent, inject, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessageBox, ElLoading } from 'element-plus' 
import PaperData from './components/PaperData.vue'


interface User {
  avatarPath: string
  name: string
}
interface Paper {
  index:number,
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
      paper: null,
      tableLoading: false,
      CurrentPage: 1,
      PageSize: 20,
      Total: 0,
      tableData:[],
    })


    const route = useRoute()
    // 获取 exam_id
    const exam_id = route.query.exam_id
    const handleButtonClickOCRPreprocess = async () => {
      console.log('OCR预处理 received id is: ', exam_id);
      const loading = ElLoading.service({
        lock: true,
        text: '处理中',
        background: 'rgba(0, 0, 0, 0.7)',
      })

      setTimeout(() => {
        loading.close()
                    ElMessageBox.alert('预处理完成！', '提示', {
                      confirmButtonText: '确定'
                    })
                    for(let i = state.tableData.length-1; i >= 0; i--) {
                      state.tableData[i]['ocr_preprocess']=1
                    }
          }, 10000);
      return

      try {
      
        const response = await axios.get(`exams/ocr_preprocess/${exam_id}/`)
        .then(function (response) {
                      console.log(response);
                      loading.close()
                      ElMessageBox.alert('预处理完成！', '提示', {
                        confirmButtonText: '确定'
                      })
                      handleUpdateValue()
                    })
                    .catch(function (error) {
                      console.log(error);
                      loading.close()
                      ElMessageBox.alert('处理失败!', '警告', {
                        confirmButtonText: '确定'
                      })
                    });
        console.log(response);
      } catch (error) {
        console.error("Error during HTTP request:", error);
      }
    }

     //查询当前页显示的表格数据
     function queryTableData() {
      let length=0
      if( state.paper !=null){
        length = state.paper.length;
        console.log('state.paper.length:',length)

      }
      state.Total=length
      state.CurrentPage = 1;
      if (length > 20) {
        state.tableData =  state.paper.slice(
          0,
          state.PageSize
        );
      } else {
        state.tableData = state.paper;
      }
    }
    // 分页
    function handlehSizeChange(val) {
      state.PageSize = val;
      state.CurrentPage = 1;
      const end = state.CurrentPage * val;
      const data = state.paper.slice(
        state.paper.length > val ? end - val : 0,
        end
      );
      state.tableData = data;
    }
    //页码发生变化时
    function handlehCurrentChange(val) {
      state.CurrentPage = Math.ceil(val);
      const end = Math.ceil(val) * state.PageSize;
      const data = state.paper.slice(end - state.PageSize, end);
      console.log(data,'data')
      state.tableData = data;
    }
        
    const handleUpdateValue = async () => {
      try {
        console.log('更新试卷数据---------------------')
        
        const response = await axios.get(`/exams/paperlist/${exam_id}/`);
        // //const response = await axios.get('exams/test/');
        state.paper = response.data;
        console.log('state.paper:',state.paper)
        console.log('response.data:', response.data)
        queryTableData()
      }catch(e) {
        console.log('Exam Error:', e)
      } 
    }
    onMounted(async() => {
      try {
        // const route = useRoute();
        // const exam_id= route.query.exam_id
        const response = await axios.get(`/exams/paperlist/${exam_id}/`);
        // //const response = await axios.get('exams/test/');
        state.paper = response.data;
        console.log('state.paper:',state.paper)
        console.log('response.data:', response.data)
        queryTableData()
      }catch(e) {
        console.log('Paper Error:', e)
      }   
    });
    return {
      state,
      handlehSizeChange,
      handlehCurrentChange,
      queryTableData,
      handleButtonClickOCRPreprocess,
      handleUpdateValue,
    }
  }
})
</script>
  