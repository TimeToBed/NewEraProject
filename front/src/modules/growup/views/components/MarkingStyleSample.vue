<template>
    <div class="w-full">
      <el-table 
      :data="tableData" 
      style="width: 100%" 
      :cell-style="{ textAlign: 'center' }"
      :header-cell-style="{ textAlign: 'center' }"
      height="320px"
      class="no-border-lines"
      >
        <el-table-column label="大模型批阅评语" min-width="75" >
          <template #default="scope">

            <el-card class="bordered-card-llm">
                <p style="font-size: 13px;">{{ scope.row.llmmarking }}</p>
            </el-card>
          </template>
        </el-table-column>
       

        <el-table-column label="教师批阅评语" min-width="75" >
          <template #default="scope">
            <el-card class="bordered-card-teacher">
                <p style="font-size: 13px;">{{ scope.row.teachermarking }}</p>
            </el-card>
          </template>
        </el-table-column>
       
        <el-table-column label="状态" min-width="30" >
          <template #default="scope">
              <div class="cursor-auto flex items-center justify-center">
                  <BadgeCheckIcon v-if="scope.row.state === 1" class="h-5 w-5 text-indigo-410"/>
                  <ExclamationCircleIcon v-if="scope.row.state === 0" class="h-5 w-5 text-red-500"/>

                  <!-- <span class="ml-2 pb-0.5 text-0.875 font-normal">{{ scope.row.state }}</span> -->
                  <span class="ml-4 pb-0.5 text-0.875 font-normal"
                        v-if="scope.row.state === 0">未学习</span>
                  <span class="ml-4 pb-0.5 text-0.875 font-normal"
                        v-if="scope.row.state === 1">已学习</span>
              </div>
          </template>
        </el-table-column>

      </el-table>
    </div>
  </template>
  <script lang="ts">
  import { defineComponent, inject } from 'vue'
  import { DotsVerticalIcon } from '@heroicons/vue/outline'
  import { AxiosInstance } from 'axios'
  import { ElMessageBox, ElLoading } from 'element-plus';
  import {BadgeCheckIcon, ExclamationCircleIcon } from '@heroicons/vue/solid'

  export default defineComponent({
    
    name: 'MarkingStyleData',
    components: {
      BadgeCheckIcon,
      ExclamationCircleIcon
    },
    
    props: {
      tableData: {
        type: Array,
        required: true,
      },
    },
    setup(props, context) {
      console.log("setup examlist")
      const axios = inject('axios') as AxiosInstance;

      return { 
        
      };
    },
    methods: {

     
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
.no-border-lines >>> .el-table__body .el-table__row td, 
.no-border-lines >>> .el-table__body .el-table__row th {
  border-top: none;
  border-bottom: none;
}

.bordered-card-llm {
  border: 1px solid green;
}

.bordered-card-teacher {
  border: 1px solid rgb(141, 11, 248);
}
</style>