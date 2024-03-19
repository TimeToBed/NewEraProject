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

      <div class="block overflow-x-auto w-full p-0">
        <el-table :data="tableData" style="width: 100%" class="is-light">
          <el-table-column label="学生姓名" min-width="200">
            <template #default="scope">
              <div class="flex items-center">
                <span class="mb-0 text-0.8125 font-semibold cursor-auto text-dark-lighter">{{
                  scope.row.pageName
                }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="成绩" min-width="150">
            <template #default="scope">
              <div class="flex items-center">
                <span class="px-4 text-0.8125 font-normal cursor-auto text-dark-lighter">{{
                  scope.row.visitorNumber
                }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="排名" min-width="150">
            <template #default="scope">
              <div class="flex items-center">
                <span class="px-4 text-0.8125 font-normal text-dark-lighter">{{
                  scope.row.userNumber
                }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="排名变化" min-width="150">
            <template #default="scope">
              <div class="flex items-center">
                <div class="px-4 flex justify-center gap-1">
                  <div>
                    <ArrowNarrowUpIcon v-if="scope.row.rate > 45.0" class="w-4 h-4 text-success" />
                    <ArrowNarrowDownIcon v-else class="w-4 h-4 text-warning" />
                  </div>

                  <span class="text-0.8125 font-normal text-dark-lighter"
                    >{{ scope.row.rate }}%</span
                  >
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
import { defineComponent } from 'vue'
import { ArrowNarrowDownIcon, ArrowNarrowUpIcon } from '@heroicons/vue/outline'

interface PageVisitInfo {
  pageName: string
  visitorNumber: string
  userNumber: number
  rate: number
}
export default defineComponent({
  name: 'PageVisitTable',
  components: {
    ArrowNarrowDownIcon,
    ArrowNarrowUpIcon,
  },
  props: {
    title: {
      type: String,
      default: '学生成绩表',
    },
  },
  setup() {
    const tableData: PageVisitInfo[] = [
      {
        pageName: '学生1',
        visitorNumber: '98',
        userNumber: 1,
        rate: 46.53,
      },
      {
        pageName: '学生2',
        visitorNumber: '96',
        userNumber: 2,
        rate: 46.53,
      },
      {
        pageName: '学生3',
        visitorNumber: '96	',
        userNumber: 3,
        rate: 36.49,
      },
      {
        pageName: '学生4',
        visitorNumber: '94',
        userNumber: 4,
        rate: 50.87,
      },
      {
        pageName: '学生5',
        visitorNumber: '89',
        userNumber: 5,
        rate: 42.53,
      },
    ]

    return {
      tableData,
    }
  },
})
</script>
