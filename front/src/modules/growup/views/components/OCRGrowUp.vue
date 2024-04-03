<template>
    <div class="h-full">
        <div class="flex justify-between py-1 px-6 border-b border-primary-white">
           <h3 class="cursor-auto">文字识别学习库</h3> 
           <div class="flex space-x-4 text-sm">
                            <p style="font-size: 14px;">当前累积样本: {{ state.num }}/{{ 10000 }}</p>
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
                        <el-button type="success" 
                        @click="handleClick"
                        :type="getButtonType()"
                        :class="getButtonClass()"
                        :disabled="isButtonDisabled()"
                        >开始学习</el-button>
                        <WaterBall class="position-relative"
                        :num="state.num" 
                        :learning="state.learning"
                        />
                    </div>
                    
                </div>
            </div>
        </div> 
        
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, reactive, computed } from 'vue'
  import WaterBall from './WaterBall.vue'
  import OCRSample from './OCRSample.vue'
  import { ElMessageBox } from 'element-plus'

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
      const state = reactive({  
        num: 6300,
        learning: false,
      })
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

      const isButtonDisabled =() => {
        return state.num<6000 || state.learning
      }

      function startInterval() {
        const interval = setInterval(() => {
          // assuming you want to decrease num by 100 every 200ms till it becomes 0
          if (state.num >= 100){ 
            state.num -= 100;
          } else {
            state.num = 0
          }
          console.log('学习中', state.num)
          if (state.num === 0){
            clearInterval(interval);
            state.learning=false
            ElMessageBox.alert('已完成学习！', '提示', {
              confirmButtonText: '确定'
            })
          }
        }, 200);
      }
      function handleClick() {
        state.learning=true;
        startInterval();
      }
      const getButtonType=() => {
        if ( state.num<6000 || state.learning){
          return ''
        }else{
          return 'primary'
        }
        
      }

      const getButtonClass=() => {
        if ( state.num<6000 || state.learning){
          return 'el-button--secondary'
        }else{
          return ''
        }
        
      }

    return {
        ocrList,
        handleClick,
        state,
        isButtonDisabled,
        getButtonType,
        getButtonClass
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