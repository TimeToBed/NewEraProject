<template>
  <div>
    <el-button class="floating-button" type="secondary" @click="openChat=true">
      <el-icon style="font-size: 24px;"><ChatLineRound /></el-icon>
    </el-button>
    <div class="chat-window" v-if="openChat">
      <div class="chat-header">
        <img src="/src/assets/images/blue.png" style="height: 20px;">
        <el-icon class="close-icon" @click="openChat=false"><Close /></el-icon>
      </div>
      <div class="chat-messages" ref="chatMessages" >
        <div  v-for="msg in messages" :key="msg.time">
          <div class="toright">
            <div class="message" v-if="msg.type=='ask'"> 
              {{ msg.text }}
            </div>
          </div>
          
          <div class="toleft">
            <div class="answer" v-if="msg.type=='answer'"> 
              {{ msg.text }}
            </div>
          </div>
        </div>
        
        <div  v-for="msg in prequestions" :key="msg.time">
          <div class="toleft prequestion" @click="handleClickPrequestion(msg.text)">
            {{ msg.text }}
        </div>
        

        </div>
      </div>
      <div class="chat-input flex">
        <el-input 
          class="message-input"
          type="textarea" 
          v-model="message" 
          @keypress.enter.exact.prevent="sendMessage" 
          placeholder="Type a message..." 
          :autosize="{ minRows: 1, maxRows: 4}"
          />
        <el-button size="small" type="primary" @click="sendMessage">
          <el-icon style="font-size: 16px;"><Promotion /></el-icon>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { ElButton, ElInput, ElIcon } from 'element-plus'
import { ChatLineRound, Close, Promotion } from '@element-plus/icons-vue';
export default {
  components: {
    ElButton,
    ElInput,
    ElIcon,
    ChatLineRound,
    Close,
    Promotion
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

      ]
    }
  },
  directives: {
    'auto-size': {
      update: function(el) {
        el.style.height = 'auto';
        el.style.height = el.scrollHeight + 'px';
      }
    }
  },

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
      "你好", 
      "苦海无边，仍欢迎你光临人间",
      "愿你一生努力，一生被爱。想要的都拥有，得不到的都释怀",
      "其实很多时候，你并不需要做什么，真诚就行",
      "总是有人要赢的，那为什么不能是我呢？",
      "平淡日子里泛着光",
      "你没有如期归来，而这正是离别的意义","生活就是既能朝九晚五，又能浪迹天涯",
      "万物皆有裂痕，那是光照进来的地方",
      "比起日出，我更想见到你",
      "如果运气不好，那就试试勇气"
    ];
    var prequestionlist=[
      "预设问题1：世界灿烂盛大，欢迎回家", 
      "预设问题2：12345", 
      "预设问题3：在温暖的阳光下，老树的影子在雪白的墙壁上慢慢地移动", 
      "预设问题4：他们一起在小路上散步，欣赏着沿途的风景", 
      "预设问题5：破晓时分，湖面上升起一层淡淡的薄雾，宛如仙境一般", 
      "预设问题6：她笑容可鞠，望着落日的余晖", 
      "预设问题7：世界灿烂盛大", 
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
          let idx=this.getRandomInt(0, answerlist.length-1)
          this.messages.push({
            text: answerlist[idx],
            time: Date.now(),
            type: "answer"
          });

          // 确保DOM更新后再滚动
          this.$nextTick(() => {
            this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight;
          });
          for (let i = 0; i < 3; i++) {
            let idx=this.getRandomInt(0, prequestionlist.length-1)
            this.prequestions.push({
              text: prequestionlist[idx],
              time: Date.now(),
              type: "prequestion"
            });
          }
          // 确保DOM更新后再滚动
          this.$nextTick(() => {
            this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight;
          });


        }, 1000); // 2000毫秒后执行，即2秒后
        
      }
    },

    handleClickPrequestion(msg){
      this.message=msg
      this.sendMessage()
    }
  }
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
  border: 1px solid #75dba3;
  border-radius: 5px;

}
.chat-header {
  padding: 10px;
  font-weight: 600;
  border-bottom: 1px solid #ccc;
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
  height: calc(100% - 120px);
  overflow-y: scroll;
  font-size: 12px;
  justify-content: flex-start;
}


.chat-messages {
  padding: 10px;
  height: calc(100% - 120px);
  overflow-y: scroll;
  font-size: 13px;
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
  border: 1px solid #d8d9d8;
  background-color: #e8ece8;
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
  border: 1px solid #c3e1c4;
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
  border: 1px solid #c3e1c4;
  background-color: #c3e1c4;
  border-radius: 10px;
  margin: 5px 25px 5px 5px;
  min-width: 60px;
  max-width: 100%;
  display: inline-block;
  word-wrap: break-word; 
  align-self: flex-start;  
  margin-right: auto;
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
</style>