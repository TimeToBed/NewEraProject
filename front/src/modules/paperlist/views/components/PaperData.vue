<template>
    <div class="w-full">
      <el-table 
      :data="tableData" 
      style="width: 100%" 
      :class="`is-${theme}`" 
      :cell-style="{ textAlign: 'center' }"
      :header-cell-style="{ textAlign: 'center' }">
        <el-table-column label="序号" min-width="60" >
          <template #default="scope">
            <div class="px-4 cursor-auto">
              <span class="text-0.8125 font-normal">{{ scope.row.index }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="考生学号" min-width="100" >
          <template #default="scope">
            <div class="px-4 cursor-auto">
              <span class="text-0.8125 font-normal">{{ scope.row.student_id }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="考生姓名" min-width="150">
          <template #default="scope">
            <div class="px-4 cursor-auto">
              <span class="text-0.8125 font-normal">{{ scope.row.student_name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="页数" min-width="60">
          <template #default="scope">
            <div class="px-4 cursor-auto">
              <span class="text-0.8125 font-normal">{{ scope.row.pages }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="批改状态" min-width="100">
          <template #default="scope">
            <div class="cursor-auto flex items-center justify-center">
              <i
                class="w-2 h-2 rounded-full"
                aria-hidden="true"
                :class="[
                  scope.row.state == 2
                    ? 'bg-info'
                    : scope.row.state == 0
                    ? 'bg-danger'
                    : scope.row.state == 1
                    ? 'bg-warning'
                    : 'bg-success',
                ]"
              ></i>
              <!-- <span class="ml-2 pb-0.5 text-0.875 font-normal">{{ scope.row.state }}</span> -->
              <span class="ml-4 pb-0.5 text-0.875 font-normal"
              v-if="scope.row.state==0">未批改</span>
              <span class="ml-4 pb-0.5 text-0.875 font-normal"
              v-if="scope.row.state==1">批改中</span>
              <span class="ml-4 pb-0.5 text-0.875 font-normal"
              v-if="scope.row.state==2">批改完</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="预处理" min-width="100">
          <template #default="scope">
              <div class="cursor-auto flex items-center justify-center">
                  <BadgeCheckIcon v-if="scope.row.ocr_preprocess === 1" class="h-5 w-5 text-indigo-410"/>
                  <ExclamationCircleIcon v-if="scope.row.ocr_preprocess === 0" class="h-5 w-5 text-red-500"/>

                  <!-- <span class="ml-2 pb-0.5 text-0.875 font-normal">{{ scope.row.state }}</span> -->
                  <span class="ml-4 pb-0.5 text-0.875 font-normal"
                        v-if="scope.row.ocr_preprocess==0">未处理</span>
                  <span class="ml-4 pb-0.5 text-0.875 font-normal"
                        v-if="scope.row.ocr_preprocess==1">已处理</span>
              </div>
          </template>
        </el-table-column>


        <!-- <el-table-column min-width="100">
          <template #default="scope">
            <el-button  type="primary" @click="handleButtonClickMarking(scope.row)">批改试卷</el-button>
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
                    <el-dropdown-item class="mx-0 hover:bg-secondary" 
                        :command="['premark',scope.row]" >
                      <div class="flex items-center w-40 h-6">
                        <span class="mb-0 text-sm">大模型预批改</span>
                      </div>
                    </el-dropdown-item>
    
                    <el-dropdown-item class="mx-0 hover:bg-secondary" 
                        :command="['marking',scope.row]"
                        >
                      <div class="flex items-center w-40 h-6">
                        <span class="mb-0 text-sm">去批改</span>
                      </div>
                    </el-dropdown-item>
                    
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </template>
          
        </el-table-column>
      </el-table>
    </div>
  </template>
  <script lang="ts">
  import { defineComponent, ref, inject } from 'vue'
  import { DotsVerticalIcon } from '@heroicons/vue/outline'
  import {BadgeCheckIcon, ExclamationCircleIcon } from '@heroicons/vue/solid'
  import { AxiosInstance } from 'axios'
  import { ElMessageBox, ElLoading } from 'element-plus';

  export default defineComponent({
    
    name: 'PaperData',
    components: {
      DotsVerticalIcon,
      BadgeCheckIcon, 
      ExclamationCircleIcon
    },
    
    props: {
      tableData: {
        type: Array,
        required: true,
      },
      totalSet: {
        type: Number,
        required: true,
      }, 
      theme: {
        type: String,
        required: false,
        default: 'light',
      },
    },
    methods: {
      handleButtonClickMarking(row) {
        console.log('批改试卷',row)
        console.log('批改试卷 paper_id',row.paper_id)
        console.log('批改试卷 totalSet',this.totalSet)
        console.log('批改试卷 totalPage',row.pages)
        this.$router.push({ 
          path: '/marking_paper', 
          query: 
            { 
              paper_id: row.paper_id , 
              totalSet: this.totalSet,
              totalPage:row.pages,
              paperData:JSON.stringify(this.tableData)
            } 
          });
      },
      
      
      handleCommand (command){
        console.log(command[0])
        console.log(command[1])
        if(command[0]=='marking'){
          this.handleButtonClickMarking(command[1])
        }else if(command[0]=='premark'){
          this.handleButtonClickPreMark(command[1])
        }
      }
    },
    setup () {
      
      const axios = inject('axios') as AxiosInstance;
      const theme = ref([
        { status: 'on schedule', color: '#11CDEF' },
        { status: 'delayed', color: '#F5365C' },
        { status: 'pending', color: '#FB6340' },
      ])
      const customColorMethod = (status: string) => {
        return theme.value.find((el: any) => el.status == status)?.color ?? '#2DCE89'
      }
      const handleButtonClickPreMark = async (row) => {
        console.log('LLM 预批改', row)
        const loading = ElLoading.service({
          lock: true,
          text: '处理中',
          background: 'rgba(0, 0, 0, 0.7)',
        })
        try {
          const response = await axios.get(`llms/llm_premark/${row.paper_id}/`)
          .then(function (response) {
                      console.log(response);
                      loading.close()
                      ElMessageBox.alert('预批改完成！', '提示', {
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
        } catch (error) {
          console.error("Error during HTTP request:", error);
        }
      };
      return {
        customColorMethod,
        handleButtonClickPreMark
      }
    }
  })
  </script>
  
<style scoped>

.header-cell {
  text-align: center;
  font-weight: bold;
}

</style>