import useStore from 'store'
import { createRouter, createWebHistory, Router } from 'vue-router'
import routes from './routes'
import { AUTH_TOKEN } from 'core/constants'

const router: Router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const store = useStore()
  store.dashboard.setIsSBOpen(false)

  // if (to.path === '/login') {
  //   if (window.innerWidth <= 768) { // 假设768px为分割点(可根据需求修改)
  //     next({ name: 'Students' })  // 如果是移动设备，导向移动登录页面
  //   } else {
  //     next({ name: 'Dashboard' })  // 否则，导向桌面登录页面
  //   }
  // } else {
  //   next() // 不是访问/login路径，不做任何操作，继续路由
  // }

  if (to.path === '/students' || to.path === '/dashboard') {
    if (!localStorage.getItem(AUTH_TOKEN)) { // 假设AUTH_TOKEN为登录密钥
      next('/login') // 如果密钥不存在（即用户未登录或已登出），导向登录页
    } else {
      next() // 如果密钥存在（即用户已登录），继续路由
    }
  } else {
    next() // 不是访问/students或/dashboard路径，不做任何操作，继续路由
  }
})

export default router
