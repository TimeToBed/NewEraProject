<template>
  <div class="w-full block mx-auto h-auto py-2">
    <div class="flex flex-wrap flex-col bg-white shadow mb-7 mx-auto rounded-md">
      <div class="py-5 px-6 border-b border-primary-white">
        <h3 class="cursor-auto">考 试 列 表</h3>
      </div>
      <div class="block overflow-x-auto w-full">
        <ExamData :tableData="state.tableData" />
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
import ExamData from './components/ExamData.vue'
import JSZip from "jszip";
import { saveAs } from 'file-saver';

interface User {
  avatarPath: string
  name: string
}
interface Exam {
  index:number,
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
      exam: null,
      tableLoading: false,
      CurrentPage: 1,
      PageSize: 10,
      Total: 0,
      tableData:[],
    })
    //查询当前页显示的表格数据
    function queryTableData() {
      let length=0
      if( state.exam !=null){
        length = state.exam.length;
        console.log('state.exam.length:',length)

      }
      state.Total=length
      state.CurrentPage = 1;
      if (length > 20) {
        state.tableData =  state.exam.slice(
          0,
          state.PageSize
        );
      } else {
        state.tableData = state.exam;
      }
    }
    // 分页
    function handlehSizeChange(val) {
      state.PageSize = val;
      state.CurrentPage = 1;
      const end = state.CurrentPage * val;
      const data = state.exam.slice(
        state.exam.length > val ? end - val : 0,
        end
      );
      state.tableData = data;
    }
    //页码发生变化时
    function handlehCurrentChange(val) {
      state.CurrentPage = Math.ceil(val);
      const end = Math.ceil(val) * state.PageSize;
      const data = state.exam.slice(end - state.PageSize, end);
      console.log(data,'data')
      state.tableData = data;
    }
    onMounted(async() => {
      try {
        const user_id= '1'
        const response = await axios.get(`exams/examlist/${user_id}/`);
        //const response = await axios.get('exams/test/');
        state.exam = response.data;
        console.log('state.exam:',state.exam)
        console.log('response.data:', response.data)
        queryTableData()
      }catch(e) {
        console.log('Exam Error:', e)
      }   
    });
    return {
      state,
      handlehSizeChange,
      handlehCurrentChange,
      queryTableData,
    }
  }
})
</script>
  