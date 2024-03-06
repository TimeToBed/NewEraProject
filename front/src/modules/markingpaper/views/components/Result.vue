<template>
  <div class="h-full">
      <el-scrollbar class="h-600">
        <ul class="no-bullet">
          <li v-for="q in questions" class="text item">
            <ResultData v-bind="q" />
          </li>          
        </ul>

      </el-scrollbar>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
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
  setup() {
    let questions=[
      {
        index: 1,
        content:"1.这是一个短问题。",
        answer:"这是一个短答案。",
        LLM_analysis:"这是一个LLM对题目的分析。",
        LLM_marking:"这是一个LLM对题目的批改。",
        LLM_score:20, 

      },

      {
        index: 1,
        content:"2.这是一个短问题。",
        answer:"这是一个短答案。",
        LLM_analysis:"这是一个LLM对题目的分析。",
        LLM_marking:"这是一个LLM对题目的批改。",
        LLM_score:10, 
      },
    ]  
    return {
      questions
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