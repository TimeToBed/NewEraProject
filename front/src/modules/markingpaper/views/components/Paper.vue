<template>
    <div class="h-full">
        <div class="h-600">
        <el-scrollbar class="h-full">
            <img src="../../../../assets/images/数据结构.png"/>
        </el-scrollbar>
        </div>
        <div class="flex justify-end">
            <el-button type="success" @click="nextForm">下一页</el-button>
        </div>
    </div>
    
    
    
</template>

<script lang="ts">
import { defineComponent } from 'vue'


export default defineComponent({
    name: 'Paper',
    methods: {
    }
})
</script>
  