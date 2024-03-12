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
        
        <el-table-column min-width="70">
          <template #default="scope">
            <!-- <el-button  type="primary" @click="handleButtonClickLLMPreprocess(scope.row)">预处理</el-button> -->
            <el-button v-if="scope.row.llm_preprocess === 1" type="primary" @click="handleButtonClickLLMPreview(scope.row)">预览</el-button>
            <el-button v-if="scope.row.llm_preprocess === 0" type="primary" @click="handleButtonClickLLMPreprocess(scope.row)">预处理</el-button>
          </template>
        </el-table-column>

        <el-table-column min-width="80">
          <template #default="scope">
            <el-button  type="primary"  @click="handleButtonClickUpload(scope.row)">上传试卷</el-button>
          </template>
        </el-table-column>

        <el-table-column min-width="80">
          <template #default="scope">
            <el-button
              :type="getButtonType(scope.row.markingable)"
              :class="getButtonClass(scope.row.markingable)"
              :disabled="isButtonDisabled(scope.row.markingable)"
              @click="handleButtonClickMarking(scope.row)">
              批改试卷
            </el-button>
          </template>
        </el-table-column>

        <el-table-column width="60" fixed="right">
          <div class="text-center h-12 pt-2.5">
            <el-dropdown placement="bottom-end" trigger="click" popper-class="action-column-popper">
              <el-button class="w-5 h-7 border-none bg-transparent hover:shadow-md" plain>
                <div class="flex items-center space-x-2 2xl:space-x-4 text-black px-5">
                  <DotsVerticalIcon class="cursor-pointer h-5 w-5 text-[#ced4da] font-extrabold" />
                </div>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu class="my-0.5">
                  <el-dropdown-item class="mx-0 hover:bg-secondary text-zinc-800">
                    <div class="flex items-center w-40 h-6">
                      <span class="mb-0 text-sm font-normal">Action</span>
                    </div>
                  </el-dropdown-item>
  
                  <el-dropdown-item class="mx-0 hover:bg-secondary text-zinc-800">
                    <div class="flex items-center w-40 h-6">
                      <span class="mb-0 text-sm font-normal">Another Action</span>
                    </div>
                  </el-dropdown-item>
  
                  <el-dropdown-item class="mx-0 hover:bg-secondary text-zinc-800">
                    <div class="flex items-center w-40 h-6">
                      <span class="mb-0 text-sm font-normal">Something else here</span>
                    </div>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-table-column>
      </el-table>
    </div>
  </template>
  <script lang="ts">
  import { defineComponent, inject } from 'vue'
  import { DotsVerticalIcon } from '@heroicons/vue/outline'
  import { AxiosInstance } from 'axios'

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
    setup() {
      const axios = inject('axios') as AxiosInstance;
      
      const handleButtonClickLLMPreprocess = async (row) => {
        console.log('LLM 预处理', row)
        try {
          const response = await axios.get(`llms/llm_preprocess/${row.exam_id}/`);
          console.log(response);
          row.llm_preprocess=1
        } catch (error) {
          console.error("Error during HTTP request:", error);
        }
      };
      
      // const handleButtonClickLLMPreview = async (row) => {
      //   console.log('LLM 预览', row)
      //   try {
      //     console.log('上传试卷',row)
      //     this.$router.push('/marking/upload_papers');

      //     const response = await axios.get(`exams/llm_preview/${row.exam_id}/`);
      //     console.log(response);



      //   } catch (error) {
      //     console.error("Error during HTTP request:", error);
      //   }
      // };

      return { 
        handleButtonClickLLMPreprocess ,
      };
    },
    methods: {

      handleButtonClickUpload(row) {
        console.log('上传试卷',row)
        this.$router.push('/marking/upload_papers');
      },
      
      handleButtonClickMarking(row) {
        console.log('批改试卷',row)
        //this.$router.push({ path: '/marking/marking_papers', query: { id: row.exam_id } });
        this.$router.push({ path: '/paperlist', query: { exam_id: row.exam_id } });
      },
      getButtonType(markingable) {
        return markingable ? 'primary' : '';
      },
      getButtonClass(markingable) {
        return markingable ? '' : 'el-button--secondary';
      },
      isButtonDisabled(markingable) {
        return !markingable;
      },
      handleButtonClickLLMPreview (row){
        console.log('LLM 预览', row)
        console.log('LLM预览',row)
        this.$router.push({path: '/previewllm', query: { exam_id: row.exam_id }});
      }
    },
  })
  </script>
  
<style scoped>

.header-cell {
  text-align: center;
  font-weight: bold;
}

</style>