<template>
      <el-card>
        <div >
            <div class="grid-items-white">
                <p class="text-title-white">题目</p>
                <br>
                <p class="text-content-white">{{ content }} </p>
            </div>

            <div class="grid-items-violet" v-if="analysis">
                <p class="text-title-violet">大模型题目分析</p>
                <br>
                <p class="text-content-violet" v-if="analysis.analysis">题目解析</p>
                <br>
                <p class="text-content-violet" v-if="analysis.analysis">{{ analysis.analysis }} </p>
                <br>
                <p class="text-content-violet" v-if="analysis.knowledge_points">知识点</p>
                <br>
                <p class="text-content-violet" v-if="analysis.knowledge_points">{{ analysis.knowledge_points }} </p>
            </div>

            <div class="grid-items-purple">
                <p class="text-title-purple">大模型批阅结果</p>
                <br>
                <p class="text-content-purple">{{ LLM_marking }} </p>
            </div>

            <div class="flex justify-between items-center"> 
                <el-input v-model="input_score" style="width: 100px" placeholder="请输入评分"  />
                <p class="text-content-white">大模型输出评分: {{ LLM_score }} </p>
            </div>

            <div class="w-full"> 
                <el-input 
                    v-model="input_comment" 
                    class="w-full" 
                    placeholder="请输入评语" 
                    type="textarea"  
                    :rows="4"
                />
            </div>
    


        </div>

      </el-card>
  </template>
  
<script lang="ts">
import { defineComponent, ref } from 'vue'
export default defineComponent({
    name: 'ResultData',
    props: {
        // 定义一个 prop 来接收数据
        content: {
            type: String, // 根据你的数据类型来设定，这里假设是 Object
            required: true // 如果是必须传递的数据，可以设定 required: true
        },

        answer: {
            type: String, 
            required: false
        },
        analysis: {
            type: Object, 
            required: true
        },
        LLM_analysis: {
            type: String, 
            required: true
        },
        LLM_marking: {
            type: String, 
            required: true
        },

        LLM_score: {
            type: String,
            required: true
        }
    },
    setup() {
        
        const input_comment = ref('')
        const input_score= ref('')

        return {
            input_comment,
            input_score
        }
    }
})
</script>

<style scoped>
.grid-items-white {
    @apply p-3 my-1 bg-white border-slate-200 
    rounded drop-shadow-[0_4px_16px_rgba(0,0,0,0.10)] 
    shadow-[0_0_0_1px_rgb(0,0,0,0.10)] text-left 
    text-sm text-gray-410 border-0 font-normal;
}


.text-title-white {
    @apply text-base text-gray-410 font-bold;
}
.text-title-white {
    @apply text-base text-gray-410 font-bold ;
    line-height:1.2rem
}
.text-content-white {
    @apply text-sm text-gray-410 font-normal ;
    line-height:1rem
}
/* .grid-items-purple {
    @apply p-3 my-1 bg-purple-200 border-slate-200 
    rounded drop-shadow-[0_4px_16px_rgba(0,0,0,0.10)] 
    shadow-[0_0_0_1px_rgb(0,0,0,0.10)] text-left 
    text-sm text-gray-410 border-0 font-normal;
} */

.grid-items-violet {
    @apply p-3 my-1 bg-violet-400 border-slate-200 
    rounded drop-shadow-[0_4px_16px_rgba(0,0,0,0.10)] 
    shadow-[0_0_0_1px_rgb(0,0,0,0.10)] text-left 
    text-sm text-white border-0 font-normal;
}
.text-title-violet {
    @apply text-base text-white font-bold ;
    line-height:1.2rem
}
.text-content-violet {
    @apply text-sm text-white font-normal ;
    line-height:1rem
}

/* .grid-items-violet {
    @apply p-3 my-1 bg-violet-200 border-slate-200 
    rounded drop-shadow-[0_4px_16px_rgba(0,0,0,0.10)] 
    shadow-[0_0_0_1px_rgb(0,0,0,0.10)] text-left 
    text-sm text-white border-0 font-normal;
}
.text-title-violet {
    @apply text-base text-gray-410 font-bold ;
    line-height:1.2rem
}
.text-content-violet {
    @apply text-sm text-gray-410 font-normal ;
    line-height:1rem
} */

.grid-items-purple {
    @apply p-3 my-1 bg-violet-500 border-slate-200 
    rounded drop-shadow-[0_4px_16px_rgba(0,0,0,0.10)] 
    shadow-[0_0_0_1px_rgb(0,0,0,0.10)] text-left 
    text-sm text-white border-0 font-normal;
}
.text-title-purple {
    @apply text-base text-white font-bold ;
    line-height:1.2rem
}
.text-content-purple {
    @apply text-sm text-white font-normal ;
    line-height:1rem
}

.card-layout {
  padding: 5;
  margin:0,0,20px,0
}
.el-card .el-card__body {
  padding: 0px !important;
}
</style>

