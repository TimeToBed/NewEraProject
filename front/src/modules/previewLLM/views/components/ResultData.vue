<template>
      <el-card>
        <div >
            <div class="grid-items-white">
                <p class="text-title-white">题目</p>
                <br>
                <p class="text-content-white">{{ content }} </p>
            </div>

            <div class="grid-items-violet" v-if="analysis">
                <p class="text-title-violet">大模型题目分析(可修改)</p>
            </div>


            <div class="w-full"> 
                <el-input 
                    v-model="llm_analysis" 
                    class="w-full" 
                    placeholder="大模型题目分析" 
                    type="textarea"  
                    :rows="4"
                    autosize="true"
                    @input="handleInput_llm_analysis"
                />
            </div>

            <div class="grid-items-purple" v-if="analysis">
                <p class="text-title-violet" v-if="analysis.knowledge_points">大模型知识点分析(可修改)</p>
            </div>
            <div class="w-full"> 
                <el-input 
                    v-model="llm_knowledge_point" 
                    class="w-full" 
                    placeholder="大模型评语" 
                    type="textarea"
                    autosize="true"  
                    :rows="4"
                    @input="handleInput_llm_knowledge_point"
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
    },
    methods: {
        handleInput_llm_knowledge_point() {
            this.analysis.change_llm_knowledge_point=this.llm_knowledge_point
            this.$emit('updateValue', this.analysis);
        },
        handleInput_llm_analysis() {
            this.analysis.change_llm_analysis=this.llm_analysis
            this.$emit('updateValue', this.analysis);
        }
    },
    setup(props) {
        let llm_knowledge_point = ref('')
        if(props.analysis?.knowledge_points){
            llm_knowledge_point = ref(props.analysis.knowledge_points)
        }
        
        let llm_analysis = ref('')
        if(props.analysis?.analysis){
            llm_analysis = ref(props.analysis.analysis)
        }

        return {
            llm_knowledge_point,
            llm_analysis
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

