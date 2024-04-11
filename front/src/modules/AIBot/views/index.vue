<template>
  <div>
    <el-button class="floating-button transition-all duration-150 hover:h-13 hover:w-13 h-12 w-12 mx-auto text-center inline-flex items-center justify-center rounded-full text-white bg-gradient-to-r from-[#8965e0] to-[#bc65e0]"
                      type="primary" @click="openChat=true">
      <el-icon style="font-size: 24px;">
        <ChatLineRound />
      </el-icon>
    </el-button>
    <div class="chat-window" v-if="openChat">
      <div class="chat-header">
        <img src="/src/assets/images/logo-ch-blue.png" style="height: 20px;">
        <el-icon class="close-icon" @click="openChat=false"><Close /></el-icon>
      </div>
      <div 
        :class="{ 'chat-messages': !state.menuVisible, 'chat-messages-short': state.menuVisible }"
        ref="chatMessages" >
        <div  v-for="msg in messages" :key="msg.time">
          <div class="toright">
            <div class="message" v-if="msg.type=='ask'"> 
              {{ msg.text }}
            </div>
          </div>

          <div class="toleft">
            <el-button
              type="success"
              plain
              style="font-size: 12px; font-weight: normal; height: 30px;border-radius: 10px;margin-left: 5px;"
              v-if="msg.type=='operation'"
              >
              <el-icon class="mr-4"> <Check /> </el-icon>
              {{ msg.text }}</el-button
            >
          </div>

          <div class="toleft">
            <div class="answer" v-if="msg.type=='answer'"> 
              {{ msg.text }}
            </div>
          </div>
        </div>
        
        <div v-for="msg in prequestions" :key="msg.time">
          <div v-if="addknowledge===0" class="toleft prequestion" @click="handleClickPrequestion(msg.text)">
            {{ msg.text }}
          </div>
        </div>
        <div v-if="addknowledge===1">
          <el-button
            type="warning"
            plain
            loading
            style="font-size: 12px; font-weight: normal; height: 30px;border-radius: 10px;margin-left: 5px;"
            
            >正在添加知识库{{ knowledgename }}</el-button
          >
        </div>
        
        <div v-if="tourl===1">
          <el-button
            type="warning"
            plain
            loading
            style="font-size: 12px; font-weight: normal; height: 30px;border-radius: 10px;margin-left: 5px;"
            
            >正在跳转界面...</el-button
          >
        </div>

      </div>
      <div class="chat-input">
        <div class="flex ">
          <el-input 
            class="message-input"
            type="textarea" 
            v-model="message" 
            @keypress.enter.exact.prevent="sendMessage" 
            placeholder="Type a message..." 
            :autosize="{ minRows: 1, maxRows: 4}"/>
            
          <el-button style="margin-left: 3px;" size="small" type="primary" @click="MenuChange">
            <el-icon style="font-size: 16px;" v-if="!state.menuVisible"><CirclePlus /></el-icon>
            <el-icon style="font-size: 16px;" v-if="state.menuVisible"><Remove /></el-icon>
          </el-button>
          <el-button style="margin-left: 3px;" size="small" type="primary" @click="sendMessage">
            <el-icon style="font-size: 16px;"><Promotion /></el-icon>
          </el-button>

        </div>
        
        
        <div class="border" v-if="state.menuVisible">
          <div class="w-full m-0">
            <div class="flex flex-wrap w-full m-0">
              <a
                
                class="flex flex-col w-1/6 py-3 text-center items-center content-center"
              >
                <div class="flex h-13 w-14 content-center items-center text-center">
                  <div class="mx-auto">
                    <div
                    class="transition-all duration-150 hover:h-10 hover:w-10 h-9 w-9 mx-auto text-center inline-flex items-center justify-center rounded-full text-white bg-gradient-to-r from-[#8965e0] to-[#bc65e0]"
                    @click="uploadKnowledge"
                    >
                    <el-icon :size="18" class="cursor-pointer w-8 h-6">
                      <Files />
                    </el-icon>
                  </div>
                  </div>
                </div>
                <span class="text-0.8125 text-black font-normal mt-1">上传外部知识库</span>
              </a>
            </div>
          </div>
        </div>
      </div>

      
      

    </div>
  </div>
</template>

<script lang="ts">
import { ElButton, ElInput, ElIcon } from 'element-plus'
import { ChatLineRound, Close, Promotion, CirclePlus, Remove,Files, Check } from '@element-plus/icons-vue';
import { ref, reactive  } from 'vue'
import { useRoute } from 'vue-router'
import { remove } from 'lodash';
export default {
  components: {
    ElButton,
    ElInput,
    ElIcon,
    ChatLineRound,
    Close,
    Promotion,
    CirclePlus,
    Remove,
    Files,
    Check
  },
  data() {
    return {
      openChat: false,
      message: '',
      messages: [{
          text: "有什么问题尽管问我吧！",
          time: Date.now(),
          type: "answer"
        }],
      prequestions: [
        { text: "如何创建一场考试？", time: Date.now(), type: "prequestion" },
         { text: "批改试卷的大模型是什么？", time: Date.now(), type: "prequestion" },
         { text: "“文心智阅”阅卷系统的优势是什么？", time: Date.now(), type: "prequestion" }

      ],
      addknowledge:0,
      knowledgename:null,
      idx:0,
      tourl: 0
    }
  },
  // directives: {
  //   'auto-size': {
  //     update: function(el) {
  //       el.style.height = 'auto';
  //       el.style.height = el.scrollHeight + 'px';
  //     }
  //   }
  // },

  methods: {
    getRandomInt: function (min, max) {
      min = Math.ceil(min);
      max = Math.floor(max);
      return Math.floor(Math.random() * (max - min + 1)) + min; // 含最大值和最小值
    },
    delayAction: function() {
      setTimeout(() => {
        // 这里写你想在延时后执行的代码
        console.log("这行代码在延时后执行");
      }, 2000); // 2000毫秒后执行，即2秒后
    },
    sendMessage() {
    var answerlist = [
      "我是文心智阅的智能机器人，依托于文心一言，可以协助你完成范围广泛的任务并提供有关各种主题的信息，比如回答问题，提供定义和解释及建议。如果你有任何问题，请随时向我提问。在“文心智阅”系统中，我还可以帮助你实现页面跳转、数据获取、外部知识库上传。", 
      "结合计算机视觉和“文心一言”大语言模型，我们的智能阅卷平台提高评阅效率，减轻教师负担，支持上传外部知识库。它全方位分析学生答案，确保评分准确性，同时评估答案逻辑和创新性，让评分更全面。其客观公正的过程具有高度解释性，既优化教学效果，也激发学生思维深度。除此之外，系统还具有“智能成长”特性，可以在批阅过程中自适应地学习教师的批改风格和文本识别能力。",
      "",
      "《红楼梦》的艺术成就可谓是中国古典小说的巅峰之作，其在继承中国古代小说艺术传统的基础上，有了巨大的创造和发展。首先，小说采用了网状形式的艺术结构，展现了高度的现实主义。全书一百二十回，上半部描述了繁华盛景，而下半部则揭示了衰败的局面，其中第五十四至第五十五回是全书由盛转衰的转折点，这种结构使得小说的情节跌宕起伏，扣人心弦。其次，人物塑造是《红楼梦》的一大艺术特色。小说成功地塑造了一批栩栩如生的人物形象，他们各自具有独特的性格和命运。",
      "《滕王阁序》是王勃的一篇骈文，它不仅以其富有画面感的描绘和深刻的思想内容展现出了作者扎实的文史功底和高端的文笔水平，还深深地揭示了古代文人对世界宇宙的理解和他们的人生哲学。“落霞与孤鹜齐飞”和“秋水共长天一色”已经成为了人们口头常提的美句。作者以滕王阁为题材，描绘出了一个壮丽的古代建筑，通过对天地、人才、壮观等的诗意描绘，展示了他对人生、命运和社会进步的深刻理解。整篇文章充满了浓厚的艺术魅力，被誉为骈文的杰出代表作。",
      
    ];
    var prequestionlist=[
      [
        "你可以给我一些建议吗？",
        "如何上传外部知识库？",
        "“文心智阅”系统的操作流程是什么？"],
        [
        "智能阅卷平台如何提升试卷评阅的效率？",
        "除了评分的准确性，智能阅卷平台还能评估学生回答的哪些方面？",
        "“智能成长”是如何学习教师的批改风格的？"],
        
        [
        "你可以给我一些建议吗？",
        "如何上传外部知识库？",
        "“文心智阅”系统的操作流程是什么？"],
        
        [
        "红楼梦的主要人物有哪些？",
        "介绍一下林黛玉的形象。",
        "《红楼梦》有哪些值得注意的细节或伏笔？"],
        
        [
        "你认为《滕王阁序》的建筑艺术有哪些特点？",
        "滕王阁序中的“落霞与孤鹜齐飞”被视为千古绝唱，你认为这反映了王勃的什么美学追求？",
        "王勃在《滕王阁序》中运用了哪些艺术手法来表现自然美？"],
        
    ];
      if (this.message !== '') {
        this.messages.push({
          text: this.message,
          time: Date.now(),
          type:"ask"
        });
        this.message = '';
        this.prequestions=[]
        this.$nextTick(() => {
          this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight;
        });
        setTimeout(() => {
        // 这里写你想在延时后执行的代码
          let idx= this.idx //this.getRandomInt(0, answerlist.length-1)
          if (idx==5){
              this.tourl=1
              
              setTimeout(() => {
                this.$router.push('/exam/create_exam');
                this.messages.push({
                  text: "已跳转到创建考试界面",
                  time: Date.now(),
                  type:"operation"
                });
                
              this.tourl=0
              }, 2000);
          }else{
            this.messages.push({
              text: answerlist[this.idx],
              time: Date.now(),
              type: "answer"
            });           
          }

          // 确保DOM更新后再滚动
          this.$nextTick(() => {
            this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight;
          });
          if(this.idx!=2){
            for (let i = 0; i < 3; i++) {
              this.prequestions.push({
                text: prequestionlist[this.idx][i],
                time: Date.now(),
                type: "prequestion"
              });
            }
          }
          
          // 确保DOM更新后再滚动
          this.$nextTick(() => {
            this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight;
          });


          this.idx+=1
        }, 1000); // 2000毫秒后执行，即2秒后
        
      }
    },

    handleClickPrequestion(msg){
      this.message=msg
      this.sendMessage()
    },
    MenuChange () {
      if (!this.state.menuVisible){
        this.state.menuVisible=true
        this.$nextTick(() => {
            this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight;
          });
      }else{
        this.state.menuVisible=false
      }
      
    },
    uploadKnowledge(){
      console.log("上传外部知识库")
      const fileInput = document.createElement('input');
      fileInput.type = 'file';
      fileInput.onchange = event => {
        const file = event.target.files[0];
        if (file) {
          console.log(file.name);
          this.knowledgename=file.name.split('.')[0]
          this.addknowledge=1
          this.state.menuVisible=false
          setTimeout(() => {
            this.messages.push({
              text: "知识库:"+this.knowledgename +"添加完成",
              time: Date.now(),
              type:"operation"
            });
          this.prequestions=[]  
          this.addknowledge=0
          this.$nextTick(() => {
            this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight;
          });
          this.idx+=1
          }, 3000);
        }
      };
      // 触发文件选择器
      fileInput.click();
    }
  },
  setup() {
    const state = reactive({  //  Vue 的响应性 API，当我们改变这个数据时，Vue 能知道需要重新渲染影响的组件。
      menuVisible:false,
      addknowledge:0,
      knowledgename:null
    });
    const route: any = useRoute()
    const clickIconMenu = ref(false)
    const fileInput = ref(null);  // 创建一个 ref
    



    return {
      route,
      clickIconMenu,
      //uploadKnowledge,
      state,
      //MenuChange,
    };
  },
}
</script>

<style scoped>
.floating-button {
  position: fixed;
  top: 600px;
  right: 10px;
  z-index: 2000;
  width: 50px;
  height: 50px;
}
.chat-window {
  z-index: 2001;
  position: fixed;
  bottom: 10px;
  right: 10px;
  background: rgb(255, 255, 255);
  width: 400px;
  height: 500px;
  border: 1px solid #650ba9c1;
  border-radius: 5px;

}
.chat-header {
  padding: 10px;
  font-weight: 600;
  border-bottom: 1px solid #eee0f3;
  position: relative;
}
.chat-header .close-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
}
.chat-messages {
  display: flex;
  flex-direction: column;
  padding: 10px;
  height: calc(100% - 100px);
  overflow-y: scroll;
  font-size: 12px;
  justify-content: flex-start;
}


.chat-messages-short {
  display: flex;
  flex-direction: column;
  padding: 10px;
  height: calc(100% - 220px);
  overflow-y: scroll;
  font-size: 12px;
  justify-content: flex-start;
}

.toright {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  width: 100%;
}
.toright {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
}

.prequestion {
  display: flex;
  justify-content: flex-start;
  padding: 5px 10px;
  border: 1px solid rgba(94, 114, 228, 0.452);
  background-color: rgba(94, 114, 228, 0.051);
  border-radius: 10px;
  margin: 5px 25px 5px 5px;
  min-width: 60px;
  max-width: 100%;
  display: inline-block;
  word-wrap: break-word; 
  align-self: flex-start;  
  margin-right: auto;
  color: #8f8c8c;
  font-size: 12px;
}

.message {
  display: flex;
  justify-content: flex-end;
  padding: 5px 10px;
  border: 1px solid rgb(94, 114, 228);
  border-radius: 10px;
  margin: 5px 5px 5px 25px;
  min-width: 60px;
  max-width: 100%;
  display: inline-block;
  word-wrap: break-word;  
  margin-left: auto;
}

.answer {
  display: flex;
  justify-content: flex-start;
  padding: 5px 10px;
  border: 1px solid rgb(94, 114, 228);
  background-color: rgb(94, 114, 228);
  border-radius: 10px;
  margin: 5px 25px 5px 5px;
  min-width: 60px;
  max-width: 100%;
  display: inline-block;
  word-wrap: break-word; 
  align-self: flex-start;  
  margin-right: auto;
  color: white;
}
.message-input {
  font-size: 12px;
}
.chat-input {
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 10px;
  border-top: 1px solid #ccc;
  background: white;
}
.chat-input el-input {
  width: calc(100% - 80px);
  float: left;
}
.chat-input el-button {
  float: right;
}

.popper {
  width: auto !important;
  min-width: 0 !important;
}
</style>