<template>
  <Topbar />
</template>

<script lang="ts">
import { defineComponent } from 'vue'

import Topbar from './components/Topbar.vue'

export default defineComponent({
  name: 'CreateExam',
  components:{
    Topbar,
  },
  data() {
    return {
    };
  },

  methods: {
  }
})
</script>
