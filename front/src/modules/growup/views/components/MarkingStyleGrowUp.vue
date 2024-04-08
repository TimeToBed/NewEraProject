<template>
  <div class="h-full">
      <div class="flex justify-between py-1 px-6 border-b border-primary-white">
         <h3 class="cursor-auto">批阅风格学习库</h3> 
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
                          <MarkingStyleSample 
                          :tableData="markingList"/>
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
import { defineComponent, reactive } from 'vue'
import WaterBall from './WaterBall.vue'
import MarkingStyleSample from './MarkingStyleSample.vue'
import { ElMessageBox } from 'element-plus'

interface MarkingData {
  llmmarking: string
  teachermarking: string
}



export default defineComponent({
  name: 'MarkingStyle',
  components: {
    WaterBall,
    MarkingStyleSample
  },
  methods: {
   
  },
  props:{
    
  },
  
  setup(props) {
    
    const state = reactive({  
        num: 2400,
        learning: false,
        sample_num:2400
      })
      state.sample_num=state.num
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
        }, 60000);
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
      
    const markingList: MarkingData[] = [
    {
      llmmarking: "学生答案完全正确，理解了儒家思想中'孝'的内涵及其在社会中的扩大过程，与原文内容相符。",
      teachermarking: "完全准确！对于儒家思想中“孝”的本质，以及其在社会中的扩大进程，真是洞若观火，理解得非常深刻，非常符合原文的核心。"
    },
    {
      llmmarking: "学生的答案是错误的。学生选择了D作为不正确的一项，但实际上根据参考解析，A选项的表述与原文不符，因此A才是正确答案。学生可能对原文的理解存在偏差，建议重新阅读原文并仔细比对选项与原文的内容。",
      teachermarking: "这个答案需要些商榷。虽然不正确的选择了D项，实质上，根据参考资料，A项才是与原文不耦合的正确答案。或许需要再静下心来，认真揣摩原文，根据文本内容，逐一比对各选项。"
    },
    {
      llmmarking: "学生答案基本正确，但未能将全部关键信息压缩进70字以内，如“天问系列”命名和寓意等部分信息可进一步简化。",
      teachermarking: "基本正确。答案应该有更好的压缩策略以适应70字上限，特别是像“天问系列”这样的关键信息，应有更高效的编写方式。"
    },
    {
      llmmarking: "学生答案完全正确，准确地补全了文中的空白处，使整段文字语意完整连贯，符合题目要求。",
      teachermarking: "太棒了！在填充空白处时，显示出了极高的精确度，完美符合这个题目的要求。"
    },
    {
      llmmarking: "学生答案错误，未能准确回忆出《离骚》中反映古代服饰“上衣下裳制”的诗句，应为“制芰荷以为衣兮，集芙蓉以为裳”。",
      teachermarking: "相信你能做的更好，从《离骚》中挑选出反映古代服饰“上衣下裳制”的诗句，准确的诗句应为：“制芰荷以为衣兮，集芙蓉以为裳”。"
    },
    {
      llmmarking: "学生答案部分正确，提到了对春光的赞美和对友人的宽慰之情，但忽略了诗中表达的不能与友人相聚的遗憾，以及对友人能够战胜病患的信心和对以后美好生活的展望，因此未能完全概括出诗歌所表达的思想感情。",
      teachermarking: "你对诗意的捕捉进步很大，不仅赞美了春光，还表达了对友人的心情抚慰，但也要注意，诗中还表达了众多其他的情感，例如对无法与友人相会的遗憾，对友人能够战胜困苦的信任，以及对未来美好生活的盼望。"
    },
    {
      llmmarking: "学生答案部分正确，理解了‘浑涵’和‘雄视’的大致含义，但在‘鲜’字的翻译上出现了遗漏，未能表达出‘罕见’的意思，且整体句子的语气未能体现出赞美之情。",
      teachermarking: "非常靠近正确答案了，理解了‘浑涵’和‘雄视’的含义，但在‘鲜’字的翻译上，需要注意，它还有一个‘罕见’的意思，而且，这个句子整体上应该充满赞美之情。"
    },
    {
      llmmarking: "学生答案在大意上基本正确，但在具体词汇的翻译上存在一些问题。例如，‘粜’应翻译为‘出售’，而不是省略；‘饘粥’应翻译为‘稠粥’，而不是简单的‘粥’。同时，‘分坊’应理解为‘分街道’，而不是‘分到各个访中’。此外，句子结构和语气也需要进一步优化，以使翻译结果更加流畅自然。",
      teachermarking: "几乎就要回答正确了，可能有些词汇的翻译需要再探索一下。比如，“粜”应该译作“出售”，不可以省略；“饘粥”更应解为“稠粥”，而非只是“粥”。另外，“分坊”应被理解为“分街道”而非“分到各个住户中”。再加上一些语气和句式的调整，一定能作出更动人的译文。"
    },
    {
      llmmarking: "学生答案中提到了小说的部分情节安排，如乔治和尼克的滑雪、在客栈喝酒和分别，但未充分结合海明威的“冰山”理论进行分析。学生只是描述了情节的顺序和描写手法，没有深入挖掘小说背后的丰富内容和隐藏的情感。因此，未能完全回答题目要求，分数扣减。",
      teachermarking: "你对情节的捕捉已经很到位了，就像乔治和尼克的滑雪、在客栈喝酒和分别，但结合海明威的“冰山”理论，可以再深一步揣摩小说的内涵与隐含的情感。有信心看到你写出更深入的分析。"
    },
    {
      llmmarking: "学生答案部分正确，分析了两人一再相约所表达的强烈愿望和依依不舍之情，但未能充分结合上下文深入分析对话者的心理变化，对于愿望能否实现的不确定性和惘然心情的表述不够充分。",
      teachermarking: "你抓住了这段对话中两个人期盼相会的渴望和不舍，但还可以尝试对对话者的心理转变进行更深入的探析，对于未来是否能实现的期待中蕴含的迷茫和感伤，也可以尝试表达出来。"
    },
  
  ]
  return {
      markingList,
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