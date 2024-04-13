<template>
  <div class="w-full">
    <el-card class="bg-gradient-to-r from-default to-dark-100">
      <template #header>
        <div class="flex flex-wrap items-center bg-transparent">
          <div class="max-w-full basis-0 grow">
            <h6 class="uppercase text-light tracking-0.625 mb-1">{{ title }}</h6>
            <h2 class="text-white mb-0">{{ subcription }}</h2>
          </div>
          <div class="max-w-full basis-0 grow">
            <div class="flex flex-nowrap mb-0 pl-0 justify-end gap-x-3">
              <!-- <div>
                <el-button type="primary" size="small" class="py-2 px-3 lh:w-20 lg:h-9"
                  @click="changeDataChart([0, 20, 10, 30, 15, 40, 20, 60])">
                  <span class="hidden md:block font-medium text-sm px-2">近半年</span>
                  <span class="md:hidden font-medium text-sm">M</span>
                </el-button>
              </div> -->
              <!-- <div>
                <el-button class="el-button--secondary py-2 px-3 lh:w-20 lg:h-9" size="small"
                  @click="changeDataChart([0, 20, 5, 25, 10, 30, 15, 40])">
                  <span class="hidden md:block text-indigo-410 font-medium text-sm px-2">近一个月</span>
                  <span class="md:hidden text-indigo-410 font-medium text-sm">W</span>
                </el-button>
              </div> -->
            </div>
          </div>
        </div>
      </template>

      <div class="card-body bg-transparent">
        <LineChart ref="salesChart" :chartData="salesData" :options="chartOptions" :height="350" />
      </div>
    </el-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, ref } from 'vue'
import { LineChart } from 'vue-chart-3'
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

export default defineComponent({
  name: 'GradientLineChart',
  components: {
    LineChart,
  },
  props: {
    title: {
      type: String,
      default: '曲线图',
    },
    subcription: {
      type: String,
      default: '学生考试平均成绩',
    },
    Datalist: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const data = props.Datalist[1]
    const salesChart = ref()
    const salesData = computed(() => ({
      labels: props.Datalist[0],
      datasets: [
        {
          label: ' 平均分数',
          tension: 0.4,
          pointRadius: 0,
          borderColor: 'rgb(94 114 228)',
          backgroundColor: 'rgba(23, 43, 77, 0.01)',
          borderWidth: 4,
          fill: true,
          data: props.Datalist[1]
        },
      ],
    }))

    const chartOptions = ref({
      scales: {
        x: {
          grid: {
            drawBorder: false,
            display: true,
            drawOnChartArea: true,
            drawTicks: true,
            // zeroLineColor: 'transparent',
            borderDash: [5, 5],
            color: 'rgb(255 255 255)',
          },
          ticks: {
            display: true,
            color: 'rgb(255 255 255)',
            padding: 20,
            font: {
              size: 14,
              family: 'Open Sans',
              style: 'normal',
              lineHeight: 2,
            },
          },
        },
        y: {
          grid: {
            drawBorder: false,
            display: true,
            drawOnChartArea: true,
            drawTicks: true,
            color: 'rgb(255 255 255)',
            borderDash: [5, 5],
          },
          ticks: {
            display: true,
            padding: 10,
            color:'rgb(255 255 255)',
            font: {
              size: 12,
              family: 'Open Sans',
              style: 'normal',
              lineHeight: 2,
            },
            callback: function (value: number) {
              if (!(value % 0.5)) {
                return `${value}分`
              }
            },
          },
        },
      },
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          callbacks: {
            label: function (context: any) {
              let label = context.dataset.label || ''
              if (label) {
                label += `: ${context.parsed.y}分`
              }
              return label
            },
          },
        },
      },
      interaction: {
        intersect: false,
        mode: 'index',
      },
    })

    const changeDataChart = (value: any) => {
      data.value = value
    }

    return {
      changeDataChart,
      salesChart,
      salesData,
      chartOptions,
    }
  },
})
</script>
