<template>
  <div class="h-full">
      <el-scrollbar class="h-600">
        <ul class="no-bullet">
          <li v-for="i in state.length" :key="i.toString()" class="text item">
            <ResultData v-bind="state.questions[i-1]" 
              @updateComment="handleUpdateComment(i-1, $event)"
              @updateScore="handleUpdateScore(i-1, $event)"/>
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
    handleUpdateComment(index, newValue) {
      // 这里的 index 和 newValue 分别是从子组件传来的索引和新值
      this.state.questions[index].comment = newValue;  // 更新相应的值
      console.log("Result.vue  this state questions[index]:",this.state.questions[index])
      this.$emit('updateValue', this.state.questions);
    }, 
    handleUpdateScore(index, newValue) {
      // 这里的 index 和 newValue 分别是从子组件传来的索引和新值
      this.state.questions[index].mark_score = newValue;  // 更新相应的值
      console.log("Result.vue  this state questions[index]:",this.state.questions[index])
      this.$emit('updateValue', this.state.questions);
    }
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