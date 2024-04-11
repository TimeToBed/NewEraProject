<template>
      <el-card>
        <div >
            <div class="grid-items-white">
                <p class="text-title-white">题目</p>
                <br>
                <p v-if="content"  class="text-content-white" v-html="content.replace(/\n/g, '<br/>')"></p>
                
            </div>


            <div class="grid-items-purple">
                <p class="text-title-purple">大模型批阅结果</p>
                <br>
                <p class="text-content-purple">{{ llm_comment }} </p>
            </div>

            <div class="flex justify-between items-center" style="height: 40px;"> 
                <div class="flex items-center">
                   <p class="text-content-white" >大模型输出评分：</p>
                    <p class="text-content-white-bold" >{{ llm_mark }}</p> 
                </div>
                
                <div class="flex items-center">
                    <p class="text-content-white" >满分：</p>
                    <p class="text-content-white-bold" >{{ score }}</p>                    
                </div>


                <div class="flex items-center">
                    <p class="text-content-white">修改评分：</p>
                    <el-input 
                        v-model="input_score" 
                        style="width: 120px" 
                        size="small"
                        placeholder="请输入评分"  
                        @input="handleInput_mark_score"
                    />
                </div>
                
                
            </div>

            <div class="w-full"> 
                <el-input 
                    v-model="input_comment" 
                    class="w-full" 
                    placeholder="请输入评语" 
                    type="textarea"  
                    :rows="4"
                    @input="handleInput_comment"
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
            type: String, 
            required: false
        },

        index: {
            type: String, 
            required: true
        },

        llm_mark: {
            type: String, // 根据你的数据类型来设定，这里假设是 Object
            required: true // 如果是必须传递的数据，可以设定 required: true
        },

        llm_comment: {
            type: String, 
            required: false
        },
        score: {
            type: Object, 
            required: true
        },
        mark: {
            type: String, 
            required: true
        },
        
        comment: {
            type: String, 
            required: true
        },

        mark_score: {
            type: String, 
            required: true
        },
    },

    methods: {
        handleInput_mark_score() {
            //this.mark_score=this.input_score
            this.$emit('updateScore', this.input_score);
            console.log('change input score:', this.input_score)
            let as_change=1
            //this.updateBorder(this.$refs.input_kp, as_change);
  
        },
        handleInput_comment() {
            //this.analysis.change_analysis=this.llm_analysis
            this.$emit('updateComment', this.input_comment);
            console.log('change input comment:', this.input_comment)
            let as_change=1
            //this.updateBorder(this.$refs.input_as, as_change);
  
        },
    },
    setup(props) {
        console.log('result data')
        let input_comment = ref(props.mark)
        let input_score= ref(props.mark_score)

        if(props?.comment){
            input_comment = ref(props.comment)
        }
        
        
        if(props?.mark_score){
            input_score = ref(props.mark_score)
        }

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

.text-content-white-bold {
    @apply text-gray-410 font-bold ;
    line-height:1rem;
    font-size:0.8rem
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
</style>

