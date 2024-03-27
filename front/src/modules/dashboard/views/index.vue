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
          <div class="baberrage">
            <vue-danmaku class="danmaku" ref="danmakuRef" v-model:danmus="danmus" useSlot loop :speeds="100" :top="50" :right="50" :fontSize="50"
              :randomChannel=true>
              <template v-slot:dm="{ danmu }">
                <div class="danmaku-name">{{ danmu }}</div>
              </template>
            </vue-danmaku>
          </div>
        </div>
        <div class="lg:flex-4 lg:max-w-1/3 w-full lg:pl-3.5">
          <SocialTrafficTable />
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

</script>

<style lang="less" scoped>
.baberrage {
  width: 100%;
  height: 400px;
  background: #ffffff;
  .danmaku {
    width: 100%;
    height: 100%;

    &-name {
      height: 100%;
      background: #f0f0f0;
      margin-right: 50px;
      color: #000000;
      --fa-font-solid: normal 900 1em / 1 "Font Awesome 6 Solid";
      --fa-font-regular: normal 400 1em / 1 "Font Awesome 6 Regular";
      --fa-font-light: normal 300 1em / 1 "Font Awesome 6 Light";
      --fa-font-thin: normal 100 1em / 1 "Font Awesome 6 Thin";
      --fa-font-duotone: normal 900 1em / 1 "Font Awesome 6 Duotone";
      --fa-font-brands: normal 400 1em / 1 "Font Awesome 6 Brands"
    }
  }
}
</style>
