
<template>
  <div class="h-full">
      <div class="h-600">
      <el-scrollbar class="h-full">
          <div ref="fileRef"></div>
      </el-scrollbar>
      </div>
      
      <div class="docWrap">
      <!-- 预览文件的地方（用于渲染） -->
        
      </div>
  </div>
  
  
  
</template>

<script lang="ts">
import { defineComponent, ref , onMounted} from 'vue'
// 引入axios用来发请求
import axios from "axios";
// 引入docx-preview插件

import { renderAsync } from 'docx-preview';

export default defineComponent({
name: 'Paper',
props:{
  file_src:{
    required: true,
  },
},
methods: {

},

setup(props){
  const fileRef = ref(null);
  onMounted(() => {
      if (fileRef.value && props.file_src) {
        renderAsync(props.file_src, fileRef.value);
      }
    });
    return { fileRef };
}
})
</script>

