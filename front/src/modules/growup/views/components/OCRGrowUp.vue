<template>
    <div class="h-full">
        <div class="flex justify-between py-1 px-6 border-b border-primary-white">
           <h3 class="cursor-auto">文字识别学习库</h3> 
           <div class="flex space-x-4 text-sm">
                            <p style="font-size: 14px;">当前累积样本: {{ 4500 }}/{{ 10000 }}</p>
                            <p style="font-size: 14px;">建议累积样本：{{ 6000 }}</p>
            </div>
        </div>
       <div class="p-4 items-center justify-center h-full">
            <div class="mt-1">
                <div class="flex flex-wrap">
                    <div class="lg:flex-8 lg:max-w-2/3 w-full lg:mb-0 lg:pr-3.5 mb-6">
                        <el-scrollbar height="320px">
                            <OCRSample 
                            :tableData="ocrList"/>
                        </el-scrollbar>
                    </div>
                    <div class="lg:flex-8 lg:max-w-1/3 w-full lg:mb-0 lg:pr-3.5 mb-6
                    h-full position-relative">
                        <el-button type="success" >开始学习</el-button>
                        <WaterBall class="position-relative"
                        :percent="46" />
                    </div>
                    
                </div>
            </div>
        </div> 
        
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, reactive } from 'vue'
  import WaterBall from './WaterBall.vue'
  import OCRSample from './OCRSample.vue'

  interface OCRData {
    img_path: string
    content: string
  }
  

  
  export default defineComponent({
    name: 'OCR',
    components: {
      WaterBall,
      OCRSample
    },
    methods: {
     
    },
    props:{
      
    },
    
    setup(props) {
      const ocrList: OCRData[] = [
      {
        img_path: "/src/assets/growup/1.png",
        content: '0又恐琼楼玉宇，高处不胜寒',
      },
    
      {
        img_path: "/src/assets/growup/2.png",
        content: '1又恐琼楼玉宇，高处不胜寒',
      },
      {
        img_path: "/src/assets/growup/3.png",
        content: '又恐琼楼玉宇，高处不胜寒',
      },
      {
        img_path: "/src/assets/growup/4.png",
        content: '又恐琼楼玉宇，高处不胜寒',
      },
      
      {
        img_path: "/src/assets/growup/5.png",
        content: '又恐琼楼玉宇，高处不胜寒',
      },
      {
        img_path: "/src/assets/growup/1.png",
        content: '0又恐琼楼玉宇，高处不胜寒',
      },
    
      {
        img_path: "/src/assets/growup/2.png",
        content: '1又恐琼楼玉宇，高处不胜寒',
      },
      {
        img_path: "/src/assets/growup/3.png",
        content: '又恐琼楼玉宇，高处不胜寒',
      },
      {
        img_path: "/src/assets/growup/4.png",
        content: '又恐琼楼玉宇，高处不胜寒',
      },
      
      {
        img_path: "/src/assets/growup/5.png",
        content: '又恐琼楼玉宇，高处不胜寒',
      },
    ]
    return {
        ocrList
    }
    },
  
  
  
  })
  </script>
  
  <style >
.no-bullet {
  list-style-type: none;
  padding: 0;
}

.el-card__body {
  padding: 10px !important;   /* 你可以改用任意你需要的尺寸 */
}
.position-relative {
    position: relative;
}
  </style>