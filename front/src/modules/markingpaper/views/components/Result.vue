<template>
  <div class="h-full">
      <el-scrollbar class="h-600"  ref="scrollbarRef" always @scroll="scroll">
        <div ref="innerRef">
          <ul class="no-bullet">
            <li v-for="i in state.length" :key="i.toString()" class="text item">
              <ResultData v-bind="state.questions[i-1]" 
                @updateComment="handleUpdateComment(i-1, $event)"
                @updateScore="handleUpdateScore(i-1, $event)"/>
            </li>    
          </ul>
        </div>
      </el-scrollbar>

      <!-- <el-slider
        v-model="value"
        :max="max"
        :format-tooltip="formatTooltip"
        @input="inputSlider"
      /> -->
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, onMounted, ref  } from 'vue'
import ResultData from './ResultData.vue';
import { ElScrollbar } from 'element-plus'

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
    },
    scrollTo(index) {
      this.$nextTick(() => {
        index=this.PagetoIndex[index]
        console.log("scrollTo element:",index)
        const items = this.$refs.innerRef.children[0].children; // 获取ul下的li元素
        console.log('items:', items)
        console.log('items[index]:',items[index])
        if (items && items[index]) {
          items[index].scrollIntoView({ behavior: 'smooth' });
          //this.$refs.scrollbarRef.scrollTop = items[index].offsetTop;
        }
      });
    }
  },
  props:{
    LLMData: {
      type: Object
    },
    page: {
      type: Number
    },
    totalPage: {
      type: Number
    }
  },

  watch: {
    page(newVal, oldVal) {
      console.log('new page:',newVal)
      this.scrollTo(newVal);
    }
  },

  setup(props) {
    const state = reactive({  //  Vue 的响应性 API，当我们改变这个数据时，Vue 能知道需要重新渲染影响的组件。
      questions:null,
      length:0,
      curIndex:0,
    })

    state.questions=props.LLMData
    state.length=Object.keys(state.questions).length;
    console.log('result.vue:', state.questions)
    console.log('result.vue length:', state.length)
    let PagetoIndex=new Array(props.totalPage).fill(-1);
    const initPage = () => {
      let lastpage=1
      PagetoIndex[1]=0
      for(let i = state.questions.length-1; i >= 0; i--) {
        PagetoIndex[state.questions[i].page]=i
      }
      for(let i=1; i<=props.totalPage; i++){
        if (PagetoIndex[i]==-1){
          PagetoIndex[i]=PagetoIndex[i-1]
        }
      }
      console.log('page to index：',PagetoIndex)
    }

    initPage()
    const max = ref(0)
    const value = ref(0)
    const innerRef = ref<HTMLDivElement>()
    const scrollbarRef = ref<InstanceType<typeof ElScrollbar>>()
    
    onMounted(() => {
      max.value = innerRef.value!.clientHeight - 380
    })
    const inputSlider = (value: number) => {
      scrollbarRef.value!.setScrollTop(value)
    }
    const scroll = ({ scrollTop }) => {
      value.value = scrollTop
    }
    const formatTooltip = (value: number) => {
      return `${value} px`
    }
    return {
      state,
      max,
      value,
      innerRef,
      scrollbarRef,
      inputSlider,
      scroll,
      formatTooltip,
      PagetoIndex
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