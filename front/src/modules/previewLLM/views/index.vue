<template>
    <Topbar 
      :exam_id="exam_id"
      />
  </template>
  
  <script lang="ts">
  import { defineComponent, onMounted, inject, reactive } from 'vue'
  import { useRoute } from 'vue-router';
  import { AxiosInstance } from 'axios';
  import Topbar from './components/Topbar.vue'
  
  export default defineComponent({
    name: 'PreviewLLM',
    components:{
      Topbar,
    },
    data() {
      return {
      };
    },
    setup() {
      const route = useRoute()
      const exam_id = Number(route.query.exam_id)
      return {
        exam_id,
      }
    },
  })
  </script>
  