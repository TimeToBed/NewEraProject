<template>
  <div class="h-full">
      <el-scrollbar class="h-600">
        <ul class="no-bullet">
          <li v-for="i in state.length" :key="i.toString()" class="text item">
            <ResultData v-bind="state.questions[i.toString()]" />
          </li>    
          <!-- <li  class="text item">
            <ResultData v-bind="state.questions['1']" />
          </li>     -->
        </ul>

      </el-scrollbar>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue'
import ResultData from './ResultData.vue';

interface Question{

}

export default defineComponent({
  name: 'Result',
  components: {
    ResultData,
  },
  methods: {

  },
  props:{
    LLMData: {
      type: Object
    }
  },
  setup(props) {
    const state = reactive({  //  Vue 的响应性 API，当我们改变这个数据时，Vue 能知道需要重新渲染影响的组件。
      questions:null,
      length:0
    })
    // let questions=[
    //   {
    //     index: 1,
    //     content:"1.这是一个短问题。",
    //     answer:"这是一个短答案。",
    //     LLM_analysis:"这是一个LLM对题目的分析。",
    //     LLM_marking:"这是一个LLM对题目的批改。",
    //     LLM_score:20, 

    //   },

    //   {
    //     index: 1,
    //     content:"2.这是一个短问题。",
    //     answer:"这是一个短答案。",
    //     LLM_analysis:"这是一个LLM对题目的分析。",
    //     LLM_marking:"这是一个LLM对题目的批改。",
    //     LLM_score:10, 
    //   },
    // ]  
    state.questions=props.LLMData
    state.length=Object.keys(state.questions).length;
    console.log('result.vue:', state.questions)
    console.log('result.vue length:', state.length)
    return {
      state,
    }
  },



})
</script>

<style >
.no-bullet {
  list-style-type: none;
  padding: 0;
}
</style>