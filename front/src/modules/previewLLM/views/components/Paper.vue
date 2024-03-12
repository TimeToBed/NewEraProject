<template>
    <div class="h-full">
        <div class="h-600">
        <el-scrollbar class="h-full">
            <img :src="img_src"/>
        </el-scrollbar>
        </div>
        
    </div>
    
    
    
</template>

<script lang="ts">
import { defineComponent } from 'vue'


export default defineComponent({
  name: 'Paper',
  props:{
    img_src:{
      type: String,
      required: true,
    },
  },
  methods: {

  },
  created (){
    console.log(this.img_src)
  }
})
</script>
  