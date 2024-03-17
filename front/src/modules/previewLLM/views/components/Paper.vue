
<template>
  <div class="h-full">
      <div class="h-600 docx-container">
      <el-scrollbar class="h-full ">
          <div class="docWrap" ref="fileRef"></div>
      </el-scrollbar>
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

<style scoped>
.docWrap {
  width: auto;
  overflow-x: auto;
  padding: 0;
}
.docx-container ::v-deep .docx-wrapper {
  background-color: #fff;
  /* padding: 20px 20px; */
}
.docx-container ::v-deep .docx-wrapper > section.docx {
  /* width: 55vw !important; */
  /* padding: 0rem !important; */
  /* min-height: auto !important; */
  box-shadow: none;
  /* margin-bottom: 0; */
  overflow-y: scroll;
  /* height: 100vh; */
}

.docx-container ::v-deep .docx-wrapper > section.docx::-webkit-scrollbar {
  display: none;
}
</style>