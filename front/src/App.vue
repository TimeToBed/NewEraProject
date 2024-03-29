<template>
  <el-config-provider :zIndex="9999" :locale="zhCn">
    <!-- <AuthLayout /> -->
    <AuthLayout v-if="isAuthLayout" />
    <DefaultLayout v-else />
  </el-config-provider>
</template>

<script lang="ts">
import { defineComponent, inject, computed } from 'vue'
import { ElConfigProvider } from 'element-plus'
import DefaultLayout from './layouts/default-layout.vue'
import AuthLayout from './layouts/auth-layout.vue'
import { useRoute, useRouter } from 'vue-router'
import locale from "element-plus/lib/locale/lang/zh-cn";

export default defineComponent({
  components: {
    DefaultLayout,
    ElConfigProvider,
    AuthLayout,
  },
  inheritAttrs: false,

  setup() {
    // console.log('万物起源',localStorage.getItem('user_id'))
    if (! localStorage.getItem('user_id')){
      //window.location.href = '/login'
      const router = useRouter();
      router.push({ path: '/login'});

    }
    const $message = inject<IMessage>('$message')
    const router = useRoute()
    const isAuthLayout = computed(() => !router.meta?.requiresAuth)
    //const isAuthLayout = !localStorage.getItem('user_id')

    const initialize = () => {
      return Promise.resolve()
    }
    initialize().catch((error: Error) => {
      $message?.error(`Couldn't initialize the system with error: ${error.message}`)
    })
    console.log('isAuthLayout:',isAuthLayout.value)
    return { zIndex: 3000, size: 'small', isAuthLayout ,zhCn: locale}
  },
})
</script>
<style>
#global-loading {
  z-index: 120000;
}
</style>
