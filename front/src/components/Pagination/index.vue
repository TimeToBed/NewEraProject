<template>
  <div class="w-full">
    <div class="flex justify-end mb-0">
      <el-pagination background layout="total, sizes, prev, pager, next, jumperprev, pager, next" :total="30" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  name: 'Pagination',
})
</script>
