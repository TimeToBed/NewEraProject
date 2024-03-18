<template>
    <div class="w-full block mx-auto h-auto py-2">
      <div class="flex flex-wrap flex-col bg-white shadow mb-7 mx-auto rounded-md">
        <div class="py-5 px-6 border-b border-primary-white">
          <h3 class="cursor-auto">造 数 据 考 试 列 表</h3>
        </div>
        <div class="mx-4 my-4">
          <el-button  type="primary"  @click="deleteAll()">删除所有伪造数据</el-button>
        </div>
        
        <el-divider ></el-divider>

        <div class="mx-20 my-10">
          <el-form  :model="formAddSetExam" class="demo-form-inline">
            <el-form-item label="开始时间">
              <el-date-picker
                v-model="formAddSetExam.startdate"
                type="date"
                placeholder="选择开始时间"
                clearable
              />
            </el-form-item>
            
            <el-form-item label="结束时间">
              <el-date-picker
                v-model="formAddSetExam.enddate"
                type="date"
                placeholder="选择结束时间"
                clearable
              />
            </el-form-item>

            <el-form-item label="等间隔">
              <el-switch v-model="formAddSetExam.isinterval" />
            </el-form-item>

            <el-form-item label="指定间隔" >
              <el-input-number
                v-model="formAddSetExam.interval"
              />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="AddSetExam">批量添加考试</el-button>
            </el-form-item>
          </el-form>

        </div>

        <el-divider ></el-divider>

        <div class="mx-4 my-4">
          <el-form :inline="true" :model="formAddStudent" class="demo-form-inline">
            <el-form-item >
              <el-input-number
                v-model="formAddStudent.number"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="AddStudent()">伪造学生</el-button>
            </el-form-item>
          </el-form>
        </div>

        <el-divider ></el-divider>

        <div class="block overflow-x-auto w-full">
          <ExamData :tableData="state.tableData"
          @updateExamList="handleUpdateValue($event)" />
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
  import { ElMessageBox } from 'element-plus'
  import ExamData from './components/ExamData.vue'
  
  
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
  
      const handleUpdateValue = async () => {
      try {
        console.log('更新数据---------------------')
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
    }


      const formAddStudent = reactive({
        number: '',
      })

      
      const formAddSetExam = reactive({
        startdate: '',
        enddate:'',
        isinterval:true,
        interval:0
      })


      const AddStudent = async () => {
        console.log('伪造指定数量的学生',formAddStudent.number)
        let form=new FormData()
        form.append('number',formAddStudent.number)
        
        console.log("伪造指定数量的学生：",form)
        const response = await axios.post('exams/fake1/', form)
        .then(function (response) {
                      console.log(response);
                      ElMessageBox.alert('已添加！', '提示', {
                        confirmButtonText: '确定'
                      })
                    })
                    .catch(function (error) {
                      console.log(error);
                      
                      ElMessageBox.alert('添加失败!', '警告', {
                        confirmButtonText: '确定'
                      })
                    });
      }

      const formatDate = (data: Date) =>{
        const y = data.getFullYear();
        const m = ("0" + (data.getMonth() + 1)).slice(-2);  // 因为JavaScript的月份是从0开始算的，所以这里我们需要加一才能得到正确的月份
        const d = ("0" + data.getDate()).slice(-2);
        return `${y}-${m}-${d}`;  // 返回格式化的日期字符串
      };

      const AddSetExam = async () => {
        console.log('批量伪造考试',formAddSetExam.startdate, formAddSetExam.enddate, formAddSetExam.interval, formAddSetExam.interval)
        let form=new FormData()
        form.append('startdate',formatDate(new Date(formAddSetExam.startdate)))
        form.append('enddate',formatDate(new Date(formAddSetExam.enddate)))
        form.append('isinterval',formAddSetExam.isinterval?1:0)
        form.append('interval',formAddSetExam.interval)
        
        console.log("伪造指定数量的学生：",form)
        const response = await axios.post('exams/fake2/', form)
        .then(function (response) {
                      console.log(response);
                      ElMessageBox.alert('已添加！', '提示', {
                        confirmButtonText: '确定'
                      })
                    })
                    .catch(function (error) {
                      console.log(error);
                      
                      ElMessageBox.alert('添加失败!', '警告', {
                        confirmButtonText: '确定'
                      })
                    });
      }

      const deleteAll = () => {
        console.log("删除所有伪造数据")
        ElMessageBox.confirm('确认删除所有伪造数据?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
        }).then(() => {
          // 这里写用户点击确定按钮后的操作
          console.log("用户点击了确定");
          const response = axios.get(`exams/fake4/` )
                    .then(function (response) {
                      console.log(response);
                      ElMessageBox.alert('已全部删除！', '提示', {
                        confirmButtonText: '确定'
                      })
                    })
                    .catch(function (error) {
                      console.log(error);
                      
                      ElMessageBox.alert('删除失败!', '警告', {
                        confirmButtonText: '确定'
                      })
                    });
        }).catch(() => {
          // 这里写用户点击取消按钮或关闭消息框后的操作
          console.log("用户点击了取消或者关闭了消息框");
        });
      };
  
      onMounted(async() => {
        try {
          const user_id= '1'
          const response = await axios.get(`exams/examlist/${user_id}/`);
          //const response = await axios.get('exams/test/');
          //state.exam = response.data;
          state.exam = response.data.map((item, index) => {
            return {
              ...item,
              number: 0  
            };
          });
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
        handleUpdateValue,
        formAddStudent,
        AddStudent,
        deleteAll,
        formAddSetExam,
        AddSetExam
      }
    }
  })
  </script>
    