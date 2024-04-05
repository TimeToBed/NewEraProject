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

      <el-table-column label="知识点分析" min-width="100">
        <template #default="scope">
            <div class="cursor-auto flex items-center justify-center">
                <BadgeCheckIcon v-if="scope.row.llm_preprocess === 1" class="h-5 w-5 text-indigo-410"/>
                <ExclamationCircleIcon v-if="scope.row.llm_preprocess === 0" class="h-5 w-5 text-red-500"/>

                <!-- <span class="ml-2 pb-0.5 text-0.875 font-normal">{{ scope.row.state }}</span> -->
                <span class="ml-4 pb-0.5 text-0.875 font-normal"
                      v-if="scope.row.llm_preprocess === 0">未分析</span>
                <span class="ml-4 pb-0.5 text-0.875 font-normal"
                      v-if="scope.row.llm_preprocess === 1">已分析</span>
            </div>
        </template>
      </el-table-column>

      <el-table-column label="批改" min-width="100">
        <template #default="scope">
          <div class="cursor-auto flex items-center justify-center">
            <i
              class="w-2 h-2 rounded-full"
              aria-hidden="true"
              :class="[
                scope.row.markingable == 2
                  ? 'bg-info'
                  : scope.row.ismarkingable == 0
                  ? 'bg-danger'
                  : scope.row.ismarkingable == 1
                  ? 'bg-warning'
                  : 'bg-success',
              ]"
            ></i>
            <!-- <span class="ml-2 pb-0.5 text-0.875 font-normal">{{ scope.row.state }}</span> -->
            <span class="ml-4 pb-0.5 text-0.875 font-normal"
            v-if="scope.row.markingable==0">待上传考卷</span>
            <span class="ml-4 pb-0.5 text-0.875 font-normal"
            v-if="scope.row.markingable==1">待分析</span>
            <span class="ml-4 pb-0.5 text-0.875 font-normal"
            v-if="scope.row.markingable==2">可批改</span>
          </div>
        </template>
      </el-table-column>
      <!-- <el-table-column min-width="70">
        <template #default="scope">
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
      </el-table-column> -->


      <el-table-column label="操作" width="120" fixed="right">
        <template #default="scope">
          <div class="text-center h-12 pt-2.5">
            <el-dropdown placement="bottom-end" trigger="click" @command="handleCommand">
              <el-button class="w-5 h-7 border-none bg-transparent hover:shadow-md" plain>
                <div class="flex items-center space-x-2 2xl:space-x-4 text-black px-5">
                  <DotsVerticalIcon class="cursor-pointer h-5 w-5 text-[#ced4da] font-extrabold" />
                </div>
              </el-button>
              
              <template #dropdown>
                <el-dropdown-menu class="my-0.5">
                  <el-dropdown-item  v-if="scope.row.llm_preprocess === 1"
                  class="mx-0 hover:bg-secondary text-zinc-800" 
                  :command="['llmpreview',scope.row]">
                    <div class="flex items-center w-40 h-6">
                      <span class="mb-0 text-sm font-normal">知识点预览</span>
                    </div>
                  </el-dropdown-item>

                  <el-dropdown-item  v-if="scope.row.llm_preprocess === 0"
                  class="mx-0 hover:bg-secondary text-zinc-800" 
                  :command="['llmpreprocess',scope.row]">
                    <div class="flex items-center w-40 h-6">
                      <span class="mb-0 text-sm font-normal">知识点分析</span>
                    </div>
                  </el-dropdown-item>

  
                  <el-dropdown-item class="mx-0 hover:bg-secondary text-zinc-800" 
                  :command="['upload',scope.row]">
                    <div class="flex items-center w-40 h-6">
                      <span class="mb-0 text-sm font-normal">上传试卷</span>
                    </div>
                  </el-dropdown-item>
  
                  <el-dropdown-item class="mx-0 hover:bg-secondary" 
                      :command="['marking',scope.row]"
                      :disabled="isButtonDisabled(scope.row.markingable)">
                    <div class="flex items-center w-40 h-6">
                      <span class="mb-0 text-sm">去批改</span>
                    </div>
                  </el-dropdown-item>
  
                  <el-dropdown-item class="mx-0 hover:bg-secondary text-zinc-800" 
                  :command="['deleteexam',scope.row]">
                    <div class="flex items-center w-40 h-6">
                      <span class="mb-0 text-sm font-normal">删除考试</span>
                    </div>
                  </el-dropdown-item>
  
                  
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </template>
        
      </el-table-column>
    </el-table>
    <UploadPapers :dialogVisible.sync="dialogVisible" :exam_id="upload_exam_id"
            @update:dialogVisible="updateDialogVisible"
            @upload:upload="update"
            ></UploadPapers>
  </div>
</template>
<script lang="ts">
import { defineComponent, inject, ref, watch } from 'vue'
import { DotsVerticalIcon } from '@heroicons/vue/outline'
import { AxiosInstance } from 'axios'
import { ElMessageBox, ElLoading } from 'element-plus';
import {BadgeCheckIcon, ExclamationCircleIcon } from '@heroicons/vue/solid'
import UploadPapers from '../../../uploadpapers/views/components/UploadPapers.vue'

export default defineComponent({
  
  name: 'ExamData',
  components: {
    DotsVerticalIcon,
    BadgeCheckIcon, 
    ExclamationCircleIcon,
    UploadPapers
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
    
    const handleButtonClickLLMPreprocess = async (row) => {
      console.log('LLM 预处理', row)
      const loading = ElLoading.service({
        lock: true,
        text: '处理中',
        background: 'rgba(0, 0, 0, 0.7)',
      })
      try {
        const response = await axios.get(`llms/llm_preprocess/${row.exam_id}/`)
        .then(function (response) {
                    console.log(response);
                    loading.close()
                    ElMessageBox.alert('预处理完成！', '提示', {
                      confirmButtonText: '确定'
                    })
                  })
                  .catch(function (error) {
                    console.log(error);
                    loading.close()
                    ElMessageBox.alert('处理失败!', '警告', {
                      confirmButtonText: '确定'
                    })
                  });
        console.log(response);
        row.llm_preprocess=1
      } catch (error) {
        console.error("Error during HTTP request:", error);
      }
    };
    

    const upload_exam_id = ref(0);

    const dialogVisible = ref(false);

    watch(dialogVisible, (newValue, oldValue) => {
      console.log('dialogVisible 变化了, 旧值: ', oldValue, ', 新值: ', newValue);
    });

    const handleButtonClickUpload = (row) => {
      dialogVisible.value = true
      // console.log('dialogVisible:', dialogVisible.value)
      upload_exam_id.value = row.exam_id // 对应到所选考试的exam_id
      console.log('exam_id:', upload_exam_id.value)
      
    };

    const updateDialogVisible = (newValue: boolean) => {
      dialogVisible.value = newValue
    };

    
    const update = (newValue: boolean) => {
      if(newValue){
        context.emit('updateExamList');
      }
    };

    const DeleteExam = (row) => {
      console.log("删除考试：",row)
      ElMessageBox.confirm('确认删除考试：'+row.exam_name+'?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(() => {
        // 这里写用户点击确定按钮后的操作
        console.log("用户点击了确定");
        const response = axios.get(`exams/delete_exam/${row.exam_id}/` )
                  .then(function (response) {
                    console.log(response);
                    ElMessageBox.alert('考试：'+row.exam_name+' 已删除！', '提示', {
                      confirmButtonText: '确定'
                    })
                    context.emit('updateExamList');
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
    return { 
      handleButtonClickLLMPreprocess ,
      DeleteExam,
      upload_exam_id,
      handleButtonClickUpload,
      updateDialogVisible,
      dialogVisible,
      update
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
    
    isButtonDisabled(markingable) {
      //console.log('批改状态', markingable, markingable==1)
      return markingable == 0;
    },
    handleButtonClickLLMPreview (row){
      console.log('LLM 预览', row)
      this.$router.push({path: '/previewllm', query: { exam_id: row.exam_id }});
    },
    handleCommand (command){
      console.log(command[0])
      console.log(command[1])
      if(command[0]=='marking'){
        this.handleButtonClickMarking(command[1])
      }else if(command[0]=='upload'){
        this.handleButtonClickUpload(command[1])
      }else if(command[0]=='llmpreview'){
        this.handleButtonClickLLMPreview(command[1])
      }else if(command[0]=='llmpreprocess'){
        this.handleButtonClickLLMPreprocess(command[1])
      }else if(command[0]=='deleteexam'){
        this.DeleteExam(command[1])
      }
    }
  },
})
</script>

<style scoped>

.header-cell {
text-align: center;
font-weight: bold;
}

.disabled-item {
color: gray !important;
}

</style>