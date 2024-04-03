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
        <el-table-column label="真实样本" min-width="60" >
          <template #default="scope">

            <el-card class="bordered-card-llm">
                <p>{{ scope.row.llmmarking }}</p>
            </el-card>
          </template>
        </el-table-column>
       

        <el-table-column label="内容" min-width="60" >
          <template #default="scope">
            <el-card class="bordered-card-teacher">
                <p>{{ scope.row.teachermarking }}</p>
            </el-card>
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