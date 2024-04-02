import useStore from 'store'
import { createRouter, createWebHistory, Router, RouteLocationNormalized, NavigationGuardNext } from 'vue-router'
import routes from './routes'

const router: Router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
  const store = useStore()
  store.dashboard.setIsSBOpen(false)

  if (window.innerWidth <= 640 && to.name == 'DesktopView') {
    next({ name: 'MobileView' })
  } else if (window.innerWidth > 640 && to.name == 'MobileView') {
    next({ name: 'DesktopView' })
  } else {
    next()
  }
})

export default router
