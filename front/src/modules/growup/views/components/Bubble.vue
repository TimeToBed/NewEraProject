<template>
    <div class="bubble-container">
      <div class="bubble" v-for="bubble in bubbles" :key="bubble">
        <el-button
            circle
            class="bubble-button w-9.85 h-9.85 bg-[#ea4c89] border-[#ea4c89] active:bg-[#ec5d94] active:border-[#ec5d94] text-white"
          >
        </el-button>
      </div>
    </div>
  </template>

<script>
export default {
  data() {
    // 创建一个冒泡的数组，可以多次复用
    return {
      bubbles: Array(20).fill(null)
    };
  },
};
</script>

<style scoped>
.bubble-container {
  position: relative;
  height: 400px;
  width: 200px;
}

.bubble {
  position: absolute;
  bottom: 0;
  animation: bubble 20s ease-in-out infinite;
}

/* 创建一个名为 bubble 动画来使气泡上升 */
@keyframes bubble {
  0% {
    bottom: 0;
  }
  100% {
    bottom: 100%;
  }
}

.bubble-button {
    background: #ea4c89;
    border: #ea4c89;
    color: white;
    width: 50px;
    height: 50px;
    position: relative;
    overflow: hidden;
    border-radius: 50%;
}

.bubble-button:before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: rgba(255, 255, 255, 0.1);
    transform: rotate(30deg);
    pointer-events: none;
    z-index: 1000;
    background: linear-gradient(
      45deg,
      rgba(255, 255, 255, 0.2) 0%,
      rgba(255, 255, 255, 0.2) 25%,
      transparent 25%,
      transparent 50%,
      rgba(255, 255, 255, 0.2) 50%,
      rgba(255, 255, 255, 0.2) 75%,
      transparent 75%,
      transparent
    );
    background-size: 50px 50px;
    animation: move 4s linear infinite;
    transform: translateX(-25px);
}

@keyframes move {
    100% {
        transform: translateX(25px);
    }
}
</style>