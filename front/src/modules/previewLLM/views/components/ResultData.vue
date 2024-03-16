<template>
      <el-card>
        <div >
            <div class="grid-items-white">
                <p class="text-title-white">题目</p>
                <!-- <br> -->
                <p class="text-content-white" v-html="content.replace(/\n/g, '<br/>')" > </p>
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
                    size="small"
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
                    :class="{ 'border-class': as_change === 1 }" 
                    placeholder="大模型评语" 
                    type="textarea"
                    autosize="true"  
                    size="small"
                    :rows="4"
                    @input="handleInput_llm_knowledge_point"
                />
            </div>
    


        </div>

      </el-card>
  </template>
  
<script lang="ts">
import { defineComponent, ref } from 'vue'
import { watch, nextTick } from 'vue';

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
    data() {
        return {
            kp_change: 0,
            as_change:0,
        };
    },
    methods: {
        handleInput_llm_knowledge_point() {
            this.analysis.change_llm_knowledge_point=this.llm_knowledge_point
            this.$emit('updateValue', this.analysis);
            this.as_change=1
            this.updateBorder()
        },
        handleInput_llm_analysis() {
            this.analysis.change_llm_analysis=this.llm_analysis
            this.$emit('updateValue', this.analysis);
            this.as_change=1
            this.updateBorder()
        },
          updateBorder() {
            if (this.as_change === 1) {
                this.$nextTick(() => {
                    this.$el.querySelector(".el-textarea__inner").style.border = "2px solid rgb(174, 0, 255)";
                });
            } else {
                this.$nextTick(() => {
                    this.$el.querySelector(".el-textarea__inner").style.border = "initial";
                });
            }
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
.border-class .el-textarea__inner {
  border: 2px solid rgb(174, 0, 255);
}

.grid-items-white {
    @apply p-3 my-1 bg-white border-slate-200 
    rounded drop-shadow-[0_4px_16px_rgba(0,0,0,0.10)] 
    shadow-[0_0_0_1px_rgb(0,0,0,0.10)] text-left 
    text-gray-410 border-0 font-normal;
    font-size:0.75rem
}


.text-title-white {
    @apply text-gray-410 font-bold;
    font-size:0.825rem
}
.text-title-white {
    @apply text-gray-410 font-bold ;
    line-height:1.2rem;
    font-size:0.825rem
}
.text-content-white {
    @apply text-gray-410 font-normal ;
    line-height:1rem;
    font-size:0.75rem
}

.grid-items-violet {
    @apply p-1 my-1 bg-violet-400 border-slate-200 
    rounded drop-shadow-[0_4px_16px_rgba(0,0,0,0.10)] 
    shadow-[0_0_0_1px_rgb(0,0,0,0.10)] text-left 
    text-white border-0 font-normal;
    font-size:0.75rem
}
.text-title-violet {
    @apply text-white ;
    line-height:1.2rem;
    font-size:0.825rem
}
.text-content-violet {
    @apply text-white font-normal ;
    line-height:1rem;
    font-size:0.75rem
}

.grid-items-purple {
    @apply p-1 my-1 bg-violet-500 border-slate-200 
    rounded drop-shadow-[0_4px_16px_rgba(0,0,0,0.10)] 
    shadow-[0_0_0_1px_rgb(0,0,0,0.10)] text-left 
    text-white border-0 font-normal;
    font-size:0.75rem
}
.text-title-purple {
    @apply text-white font-bold ;
    line-height:1.2rem;
    font-size:0.825rem
}
.text-content-purple {
    @apply text-white font-normal ;
    line-height:1rem;
    font-size:0.75rem
}

.card-layout {
  padding: 5;
  margin:0,0,20px,0
}
.el-card .el-card__body {
  padding: 0px !important;
}

.w-full.my-input .el-input__inner {
  font-size: 13px;
}
/* .custom-input {
  font-size: 13px;
}
.el-textarea__inner {
    font-size: 13px;
} */

.custom-input .el-input__inner textarea.el-textarea {
  font-size: 13px !important;
}
</style>

