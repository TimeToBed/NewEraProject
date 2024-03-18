<template>
    <div class="w-full">
      <el-table 
      :data="tableData" 
      style="width: 100%" 
      :class="`is-${theme}`" 
      :cell-style="{ textAlign: 'center' }"
      :header-cell-style="{ textAlign: 'center' }"
      >
        <el-table-column label="序号" min-width="60" >
          <template #default="scope">
            <div class="px-4 cursor-auto">
              <span class="text-0.8125 font-normal">{{ scope.row.index }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="考试名称" min-width="200" >
          <template #default="scope">
            <div class="px-4 cursor-auto">
              <span class="text-0.8125 font-normal">{{ scope.row.exam_name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="考试时间" min-width="120">
          <template #default="scope">
            <div class="px-4 cursor-auto">
              <span class="text-0.8125 font-normal">{{ scope.row.exam_date }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="科目" min-width="80">
          <template #default="scope">
            <div class="px-4 cursor-auto">
              <span class="text-0.875 font-normal">{{ scope.row.subject }}</span>
            </div>
          </template>
        </el-table-column>
        
        
        <el-table-column min-width="200">
          <template #default="scope">
            <el-form :inline="true" :model="scope.row" class="demo-form-inline">
              <el-form-item >
                <el-input-number
                  v-model="scope.row.number"
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="AddPapersforExam(scope.row)">添加考卷</el-button>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>

        <!-- <el-table-column min-width="80">
          <template #default="scope">
            <el-button  type="primary"  @click="AddPapersforExam(scope.row)">添加试卷</el-button>
          </template>
        </el-table-column> -->

      </el-table>
    </div>
  </template>
  <script lang="ts">
  import { defineComponent, inject, reactive } from 'vue'
  import { DotsVerticalIcon } from '@heroicons/vue/outline'
  import { AxiosInstance } from 'axios'
  import { ElMessageBox } from 'element-plus';

  export default defineComponent({
    
    name: 'ExamData',
    components: {
      DotsVerticalIcon,
    },
    
    props: {
      tableData: {
        type: Array,
        required: true,
      },
      theme: {
        type: String,
        required: false,
        default: 'light',
      },
    },
    setup(props, context) {
      console.log("setup examlist")
      const axios = inject('axios') as AxiosInstance;

           
      // const formAddPapersforExam = reactive({
      //   number: '',
      // })

      const AddPapersforExam = async (row) => {
        console.log('伪造指定数量的数据', row)
        let form=new FormData()
        form.append('exam_id',row.exam_id)
        form.append('number',row.number)
        console.log("伪造指定数量的数据：",form)
        const response = await axios.post('exams/fake3/', form).then(function (response) {
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

      return { 
        AddPapersforExam ,
      };
    },

  })
  </script>
  
<style scoped>

.header-cell {
  text-align: center;
  font-weight: bold;
}

</style>