<template>
  <div class="w-full">
    <div class="grid lg:grid-cols-12 md:grid-cols-6 sm:grid-cols-3 gap-7">
      <div class="col-span-3">
        <el-card
          class="border-white"
          :body-style="{ 'padding-top': '16px', 'padding-bottom': '16px' }"
        >
          <div class="flex flex-wrap">
            <div class="basis-0 grow">
              <div class="card-header">
                <h5 class="font-semibold text-0.8125 text-muted mb-0">学生数量</h5>
              </div>
              <h2 class="text-xl textindigo-210 font-semibold mb-0 leading-7.5">{{Datalist[0]}}</h2>
            </div>
            <div
              class="w-12 h-12 text-center inline-flex items-center justify-center rounded-full text-white bg-gradient-to-r from-[#f5365c] to-[#f56036]"
            >
              <font-awesome-icon :icon="['fas', 'hand-point-up']" size="lg" />
            </div>
          </div>
        </el-card>
      </div>
      <div class="col-span-3">
        <el-card
          class="border-white"
          :body-style="{ 'padding-top': '16px', 'padding-bottom': '16px' }"
        >
          <div class="flex flex-wrap">
            <div class="basis-0 grow">
              <div class="card-header">
                <h5 class="font-semibold text-0.8125 text-muted mb-0">考试次数</h5>
              </div>
              <h2 class="text-xl textindigo-210 font-semibold mb-0 leading-7.5">{{Datalist[1]}}</h2>
            </div>
            <div
              class="w-12 h-12 text-center inline-flex items-center justify-center rounded-full text-white bg-gradient-to-r from-[#fb6340] to-[#fbb140]"
            >
              <font-awesome-icon :icon="['fas', 'chart-pie']" size="lg" />
            </div>
          </div>
        </el-card>
      </div>
      <div class="col-span-3">
        <el-card
          class="border-white"
          :body-style="{ 'padding-top': '16px', 'padding-bottom': '16px' }"
        >
          <div class="flex flex-wrap">
            <div class="basis-0 grow">
              <div class="card-header">
                <h5 class="font-semibold text-0.8125 text-muted mb-0">批改试卷量</h5>
              </div>
              <h2 class="text-xl textindigo-210 font-semibold mb-0 leading-7.5">{{Datalist[2]}}</h2>
            </div>

            <div
              class="w-12 h-12 text-center inline-flex items-center justify-center rounded-full text-white bg-gradient-to-r from-[#2dce89] to-[#2dcecc]"
            >
              <font-awesome-icon :icon="['fas', 'coins']" size="lg" />
            </div>
          </div>
        </el-card>
      </div>
      <div class="col-span-3">
        <el-card
          class="border-white"
          :body-style="{ 'padding-top': '16px', 'padding-bottom': '16px' }"
        >
          <div class="flex flex-wrap">
            <div class="basis-0 grow">
              <div class="card-header">
                <h5 class="font-semibold text-0.8125 text-muted mb-0">进步人数占比</h5>
              </div>
              <h2 class="text-xl textindigo-210 font-semibold mb-0 leading-7.5">{{Datalist[3]}}%</h2>
            </div>
            <div
              class="w-12 h-12 text-center inline-flex items-center justify-center rounded-full text-white bg-gradient-to-r from-[#11cdef] to-[#1171ef]"
            >
              <font-awesome-icon :icon="['fas', 'chart-simple']" size="lg" />
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue'
import { ArrowUpIcon } from '@heroicons/vue/solid'

export default defineComponent({
  name: 'AnalysisCard',
  components: {
    ArrowUpIcon,
  },
  props: {
    Datalist: {
        type: Object,
        required: true,
      },
  },
  setup() {
    return {}
  },
})
</script>
