<template>
  <div class="w-full mx-auto">
    <div class="w-full">
      <AnalysisCard />
    </div>

    <div class="mt-6">
      <div class="flex flex-wrap">
        <div class="lg:flex-8 lg:max-w-2/3 w-full lg:mb-0 lg:pr-3.5 mb-6">
          <GradientLineChart />
        </div>
        <div class="lg:flex-4 lg:max-w-1/3 w-full lg:pl-3.5">
          <TotalBarChart />
        </div>
      </div>
    </div>

    <div class="mt-6">
      <div class="flex flex-wrap">
        <div class="lg:flex-8 lg:max-w-2/3 w-full lg:mb-0 lg:pr-3.5">
          <PageVisitTable />
        </div>
        <div class="lg:flex-4 lg:max-w-1/3 w-full lg:pl-3.5">
          <SocialTrafficTable />
        </div>
      </div>
    </div>
    <div class="mt-6">
      <div class="flex flex-wrap">
        <div class="lg:flex-8 lg:max-w-2/3 w-full lg:mb-0 lg:pr-3.5">
          <div class="carousel">
            <el-carousel height="400px">
              <el-carousel-item v-for="item in danmus" :key="item">
                <h3 class="carousel-text" text="2xl"
                  :style="[{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }, { color: colors[Math.round(Math.random() * 20)] }]">
                  {{ item }}</h3>
              </el-carousel-item>
            </el-carousel>
          </div>
        </div>
        <div class="lg:flex-4 lg:max-w-1/3 w-full lg:pl-3.5">
          <div class="baberrage">
            <vue-danmaku class="danmaku" ref="danmakuRef" v-model:danmus="danmus" useSlot loop :speeds="100" :top="50"
              :right="50" :fontSize="50" :randomChannel=true>
              <template v-slot:dm="{ danmu }">
                <div :style="{ color: colors[Math.round(Math.random() * 20)] }">{{ danmu }}</div>
              </template>
            </vue-danmaku>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

import AnalysisCard from 'modules/cards/views/components/AnalysisCard.vue'
// Chart
import GradientLineChart from './components/GradientLineChart.vue'
import TotalBarChart from './components/TotalBarChart.vue'
// Table
import SocialTrafficTable from './components/SocialTrafficTable.vue'
import PageVisitTable from './components/PageVisitTable.vue'

export default defineComponent({
  name: 'DashBoard',
  components: {
    AnalysisCard,
    GradientLineChart,
    TotalBarChart,
    PageVisitTable,
    SocialTrafficTable,
  },
})
</script>

<script lang="ts" setup>
import vueDanmaku from 'vue3-danmaku'
import { ref, computed } from 'vue'

const danmus = ref([
  '今天天气不错，适合出去散步。',
  '明天有个重要的会议，需要准备一下。',
  '中午吃什么好呢？我想吃火锅。',
  '这个周末打算去旅游，还没定好目的地。',
  '最近在学习一门新的技术，挺有意思的。',
  '生活总是充满了各种各样的惊喜。',
  '时间过得真快，转眼间又到了周末。',
  '每天都要保持好心情，生活才会更美好。'
])

const colors = ref([
  "#ffb980",
  "#2ec7c9",
  "#5ab1ef",
  "#b6a2de",
  "#d87a80",
  "#8d98b3",
  "#e5cf0d",
  "#97b552",
  "#95706d",
  "#dc69aa",
  "#07a2a4",
  "#9a7fd1",
  "#588dd5",
  "#f5994e",
  "#c05050",
  "#59678c",
  "#c9ab00",
  "#7eb00a",
  "#6f5553",
  "#c14089",
  "#409eff",])
</script>

<style lang="less" scoped>
.baberrage {
  width: 100%;
  height: 400px;
  background: #ffffff;

  .danmaku {
    width: 100%;
    height: 100%;

    &-name {}
  }
}

.carousel {
  display: block;
  text-align: center;
  width: 100%;
  height: 400px;

}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
