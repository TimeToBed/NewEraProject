<template>
  
    <div class="w-full block mx-auto h-auto py-2">
      <div class="flex-wrap flex-row bg-white shadow mb-2 mx-auto rounded-md">
        <div class="flex justify-between py-2 px-6 border-b border-primary-white">
           <h3 class="cursor-auto">智能生长</h3> 
        </div>
        
      <div class="p-2 flex flex-col w-full h-860">
        <div class="p-2 m-2 flex-1 lg:max-h-1/2 border h-400">
            <OCR />
        </div>
        <div class="p-2 m-2 flex-1 lg:max-h-1/2 border h-400">
            <MarkingStyle />
        </div>
    </div>
  
        
  
      </div>
      
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, inject, reactive, ref ,nextTick} from 'vue'
  import MarkingStyle from './components/MarkingStyleGrowUp.vue'
  import OCR from './components/OCRGrowUp.vue'
  import { AxiosInstance } from 'axios'
  import { ElMessageBox, ElLoading } from 'element-plus';

  
  export default defineComponent({
    name: 'GrowUp',
    components: {
      MarkingStyle,
      OCR
    },
    props:{
      
    },
  
    methods: {

    },
    setup(props){
      
     
  
      return {
        
      }
    }
  })
  </script>
  