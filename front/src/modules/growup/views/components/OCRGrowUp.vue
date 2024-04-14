<template>
    <div class="h-full" 
        
        >
        <!-- <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.5);">
          <el-progress type="circle" :percentage="50"></el-progress>
        </div> -->
    <!-- <div class="h-full d-flex align-center justify-center" 
        v-loading="true"
        element-loading-text="学习中..."
      > -->
        <div class="flex justify-between py-1 px-6 border-b border-primary-white">
           <h3 class="cursor-auto">文字识别学习库</h3> 
           <div class="flex space-x-4 text-sm">
                            <p style="font-size: 14px;">当前累积样本: {{ state.sample_num }}/{{ 10000 }}</p>
                            <p style="font-size: 14px;">建议累积样本：{{ 6000 }}</p>
            </div>
        </div>
       <div class="p-4 items-center justify-center h-full">
            <div class="mt-1">
                <div class="flex flex-wrap">
                    <div class="lg:flex-8 lg:max-w-2/3 w-full lg:mb-0 lg:pr-3.5 mb-6">
                        <el-scrollbar height="320px">
                            <OCRSample 
                            :tableData="state.ocrList"/>
                        </el-scrollbar>
                    </div>
                    <div class="flex lg:flex-8 lg:max-w-1/3 w-full lg:mb-0 lg:pr-3.5 mb-6
                      h-full position-relative" >
                      <!-- <div>
                        <Bubble />
                      </div> -->
                      <div 
                      >
                          <el-button type="success" 
                          @click="handleClick"
                          :type="getButtonType()"
                          :class="getButtonClass()"
                          :disabled="isButtonDisabled()"
                          v-if="!state.learning"
                          >开始学习</el-button>

                          
                          <el-button type="success" 
                          @click="handleClick"
                          :type="getButtonType()"
                          :class="getButtonClass()"
                          :disabled="isButtonDisabled()"
                          v-if="state.learning"
                          >正在学习</el-button>

                          <WaterBall class="position-relative "
                          :num="state.num" 
                          :learning="state.learning"
                          />
                      </div>

                      <div v-if="loading">
                        <Bubble />
                      </div>  
                    </div>
                    
                    
                    
                </div>
            </div>
        </div> 
        
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, reactive, computed, ref } from 'vue'
  import WaterBall from './WaterBall.vue'
  import OCRSample from './OCRSample.vue'
  import { ElMessageBox } from 'element-plus'
  import Bubble from './Bubble.vue'
  interface OCRData {
    img_path: string
    content: string
    state: Number
  }
  

  
  export default defineComponent({
    name: 'OCR',
    components: {
      WaterBall,
      OCRSample,
      Bubble
    },
    methods: {

    },
    props:{
      
    },
    
    setup(props) {
      const state = reactive({  
        num: 6300,
        learning: false,
        sample_num:0,
        ocrList:[]
      })
      state.sample_num=state.num
      const loading = ref(false)
      const ocrList: OCRData[] = [
      {
        img_path: "/src/assets/growup/1.png",
        content: '又恐琼楼玉宇，高处不胜寒',
        state: 0,
      },
    
      {
        img_path: "/src/assets/growup/2.png",
        content: '剑外忽传收蓟北',
        state: 0,
      },
      {
        img_path: "/src/assets/growup/3.png",
        content: '制芰荷以为衣兮，集芙蓉以为裳',
        state: 0,
      },
      {
        img_path: "/src/assets/growup/4.png",
        content: '举头望明月，低头思故乡',
        state: 0,
      },
      
      {
        img_path: "/src/assets/growup/5.png",
        content: '关山难越，谁悲失路之人',
        state: 0,
      },
      {
        img_path: "/src/assets/growup/6.png",
        content: '萍水相逢，尽是他乡之客',
        state: 0,
      },
    
      {
        img_path: "/src/assets/growup/7.png",
        content: '人生如逆旅',
        state: 0,
      },
      {
        img_path: "/src/assets/growup/8.png",
        content: '又恐琼楼玉宇，高处不胜寒',
        state: 0,
      },
      {
        img_path: "/src/assets/growup/9.png",
        content: '又恐琼楼玉宇，高处不胜寒',
        state: 0,
      },
      
      {
        img_path: "/src/assets/growup/10.png",
        content: '又恐琼楼玉宇，高处不胜寒',
        state: 0,
      },
    ]
      state.ocrList=ocrList
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
            state.sample_num=0
            ElMessageBox.alert('已完成学习！', '提示', {
              confirmButtonText: '确定'
            })
          }
        }, 1000);
      }
      function handleClick() {
        state.learning=true;
        loading.value=true
        //startInterval();
        setTimeout(() => {
          state.learning=false
          state.sample_num=0
          state.num=0
          loading.value=false
          for(let i = 0; i <state.ocrList.length-1; i++) {
            state.ocrList[i]['state']=1
          }
          ElMessageBox.alert('已完成学习！', '提示', {
            confirmButtonText: '确定'
          })
        }, 30000);
        const interval = setInterval(() => {
          
         
            clearInterval(interval);
            
          
        }, 30000);
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
        getButtonClass,
        loading
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