<template>
  <Topbar 
    v-if="paperData" 
    :paper_id="paper_id"
    :totalSet="totalSet"
    :totalPage="totalPage"
    :paperData="paperData"
    />
</template>

<script lang="ts">
import { defineComponent, onMounted, inject, reactive } from 'vue'
import { useRoute } from 'vue-router';
import { AxiosInstance } from 'axios';
import Topbar from './components/Topbar.vue'

export default defineComponent({
  name: 'MarkingPaper',
  components:{
    Topbar,
  },
  data() {
    return {
    };
  },
  setup() {
    const route = useRoute()
    const paper_id = Number(route.query.paper_id)
    const totalSet=Number(route.query.totalSet)
    const totalPage=Number(route.query.totalPage)
    const paperData=JSON.parse(route.query.paperData)
    console.log('marking paper paperData:', paperData)
    return {
      paper_id,
      totalSet,
      totalPage,
      paperData
    }
  },
})
</script>
