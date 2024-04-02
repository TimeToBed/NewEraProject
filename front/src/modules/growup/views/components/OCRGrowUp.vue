<template>
    <div class="h-full">
        <div class="flex justify-between py-1 px-6 border-b border-primary-white">
           <h3 class="cursor-auto">文字识别学习库</h3> 
        </div>
       <div class="p-4 items-center justify-center h-full">
            <div class="mt-1">
                <div class="flex flex-wrap">
                    <div class="lg:flex-8 lg:max-w-2/3 w-full lg:mb-0 lg:pr-3.5 mb-6">
                        <el-scrollbar height="360px">
                            <ul class="no-bullet">
                                <li v-for="i in 10" :key="i.toString()">
                                    <el-card >
                                        <div class="flex space-x-4">
                                            <div>
                                                <img src="@/assets/growup/1.png">
                                            </div>
                                            <div>
                                                又恐琼楼玉宇，高处不胜寒
                                            </div>
                                        </div>
                                        
                                    </el-card>
                                    
                            
                                </li>    
                            </ul>

                        </el-scrollbar>
                    </div>
                    
                </div>
            </div>
        </div> 
        
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, reactive } from 'vue'

  

  
  export default defineComponent({
    name: 'OCR',
    components: {
      
    },
    methods: {
     
    },
    props:{
      
    },
    setup(props) {
     
    },
  
  
  
  })
  </script>
  
  <style >
.no-bullet {
  list-style-type: none;
  padding: 0;
}
  </style>