<template>
  <div class="w-full">
    <div class="flex flex-wrap flex-col bg-white shadow mb-7 mx-auto rounded-md">
      <div class="flex flex-wrap items-center py-2 px-6 mb-0 border-b-dark-4">
        <div class="max-w-full basis-0 grow">
          <h3 class="mb-0 cursor-auto text-primary-dark">{{ title }}</h3>
        </div>
        <div class="max-w-full basis-0 grow">
          <div class="flex flex-wrap mb-0 pl-0 justify-end gap-x-3">
            <div>
              <el-button type="primary" size="small"> See all </el-button>
            </div>
          </div>
        </div>
      </div>

      <div class="block overflow-x-auto w-full">
        <el-table :data="tableData" style="width: 100%" class="is-light">
          <el-table-column label="题目类型" min-width="120">
            <template #default="scope">
              <div class="flex items-center">
                <span class="mb-0 text-0.8125 font-semibold cursor-auto text-dark-lighter">{{
                  scope.row.referral
                }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="平均得分" width="110">
            <template #default="scope">
              <div class="flex items-center">
                <span class="px-4 text-0.8125 font-normal text-dark-lighter">{{
                  scope.row.visitorNumber
                }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="失分率" min-width="200">
            <template #default="scope">
              <div class="px-4 flex flex-row items-center">
                <div class="w-2/5 text-right">
                  <span class="text-0.8125">{{ scope.row.completion }}%</span>
                </div>
                <div class="w-full ml-2">
                  <el-progress
                    :percentage="scope.row.completion"
                    :show-text="false"
                    :color="customColorMethod(scope.row.completion)"
                  />
                </div>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'SocialTrafficTable',
  props: {
    title: {
      type: String,
      default: '各类型题目失分率',
    },
  },
  setup() {
    const tableData: any[] = [
      {
        referral: '单选题',
        visitorNumber: '13',
        completion: 30,
      },
      {
        referral: '多选题',
        visitorNumber: '10',
        completion: 40,
      },
      {
        referral: '古诗文默写',
        visitorNumber: '18',
        completion: 10,
      },
      {
        referral: '文言文',
        visitorNumber: '19',
        completion: 30,
      },
      {
        referral: '阅读理解',
        visitorNumber: '25',
        completion: 20,
      },
      {
        referral: '作文',
        visitorNumber: '48',
        completion: 10,
      },
    ]
    const theme = ref([
      { completion: 10, color: '#6c6be4' },
      { completion: 20, color:  '#2DCE89'},
      { completion: 30, color:  '#11CDEF'},
      { completion: 40, color: '#F5365C' },
    ])

    const customColorMethod = (completion: number) => {
      return theme.value.find((el: any) => el.completion == completion)?.color ?? '#FB6340'
    }

    return {
      tableData,
      customColorMethod,
    }
  },
})
</script>
