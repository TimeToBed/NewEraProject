<template>
  <div class="w-full">
    <div class="flex flex-wrap flex-col bg-white shadow mb-7 mx-auto rounded-md">
      <div class="flex flex-wrap items-center py-2 px-6 mb-0 border-b-dark-4">
        <div class="max-w-full basis-0 grow">
          <h3 class="mb-0 cursor-auto text-primary-dark">{{ title }}</h3>
        </div>
      </div>

      <div class="block overflow-x-auto w-full">
        <el-table :data="tableData.value" style="width: 100%" class="is-light">
          <!-- <el-table-column label="题目类型" min-width="120">
            <template #default="scope">
              <div class="flex items-center">
                <span class="mb-0 text-0.8125 font-semibold cursor-auto text-dark-lighter">{{
                  scope.row.referral
                }}</span>
              </div>
            </template>
          </el-table-column> -->
          <el-table-column label="题目类型" min-width="110" align="center" height="16rem">
            <template #default="scope">
              <div class="flex items-center">
                <span class="px-4 text-0.8125 font-normal text-dark-lighter">{{
                  scope.row.name
                }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="失分率" min-width="200"  align="center">
            <template #default="scope">
              <div class="px-4 flex flex-row items-center">
                <div class="w-2/5 text-right">
                  <span class="text-0.8125">{{ 100-scope.row.score }}%</span>
                </div>
                <div class="w-full ml-2">
                  <el-progress :percentage="100-scope.row.score" :show-text="false"
                    :color="customColorMethod(100-scope.row.score)" />
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
import { defineComponent, ref,computed } from 'vue'

export default defineComponent({
  name: 'SocialTrafficTable',
  props: {
    title: {
      type: String,
      default: '各类型题目失分率',
    },
    Datalist: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    // 使用computed创建一个响应式引用，确保对Datalist的变化进行响应
    const tableData = computed(() => props.Datalist);
    const theme = ref([
      { completion: 10, color: '#6c6be4' },
      { completion: 20, color: '#2DCE89' },
      { completion: 30, color: '#11CDEF' },
      { completion: 40, color: '#F5365C' },
    ])
    const customColorMethod = (completion: number) => {
      return theme.value.find((el: any) => el.completion == completion)?.color ?? '#FB6340'
    }
    return {
      tableData,
      theme,
      customColorMethod
    };
  },
})
</script>
