<template>
<div class="bubble-container">
  <div class="bubble" 
       v-for="bubble in bubbles" 
       :key="bubble.delay" 
       :style="{ '--delay': bubble.delay, '--left': bubble.left }" 
  >
    <img src='@/assets/images/bubble.png' 
         style="height: 10px;width: 10px;">
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      bubbles: Array.from({length: 10}, () => ({
        delay: Math.random() * 10 + "s",
        left: Math.random() * 80 + "%"
      })),
      timer: null,  // 给定时器一个初始值
    }
  },
  mounted() {
    this.timer = setInterval(() => {
      this.bubbles.push({
        delay: Math.random() /0.2 + "s",
        left: Math.random() * 80 + "%"
      });
      if(this.bubbles.length > 30) this.bubbles.shift(); 
    }, 2000);
  },
  beforeDestroy() {
    clearInterval(this.timer);  // 在实例被销毁前清除定时器
  }
}
</script>

<style scoped>
.bubble-container {
  position: absolute;
  left: 0%;
  top: 25%;
  height: 280px;
  width: 400px;
  z-index: 9999;
}

.bubble {
  position: absolute;
  bottom: 0;
  animation: bubble 5s linear infinite;
  animation-delay: var(--delay); 
  left: var(--left);  
}
/* 创建一个名为 bubble 动画来使气泡上升 */
@keyframes bubble {
  0% {
    bottom: 0;
    transform: scale(1);
  }
  100% {
    bottom: 100%;
    transform: scale(3);
  }
}


@keyframes move {
    100% {
        transform: translateX(25px);
    }
}
</style>