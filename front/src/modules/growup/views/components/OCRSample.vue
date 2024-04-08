<template>
    <div class="w-full">
      <el-table 
      :data="tableData" 
      style="width: 100%" 
      :cell-style="{ textAlign: 'center' }"
      :header-cell-style="{ textAlign: 'center' }"
      height="320px"
      >
        <el-table-column label="OCR图像" min-width="60" >
          <template #default="scope">
            <div class="px-4 cursor-auto">
                <img :src="scope.row.img_path" :style="{ 'height': '30px', 'object-fit': 'cover'}">
                                            
            </div>
          </template>
        </el-table-column>
       

        <el-table-column label="正确标签" min-width="60" >
          <template #default="scope">
            <div class="px-4 cursor-auto">
              <span class="text-0.8125 font-normal">{{ scope.row.content }}</span>
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
    
    name: 'ExamData',
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

</style>