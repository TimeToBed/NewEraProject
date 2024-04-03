import { defineStore } from 'pinia'
import { ILogin } from './types'
import { AUTH_TOKEN } from 'core/constants'




export const useActions = defineStore('auth.actions', () => {
  const actLogin = async (_: ILogin) => {
    localStorage.setItem(AUTH_TOKEN, 'user') 
    if (window.innerWidth <= 768) {
      //如果是移动设备
      window.location.href = '/students'
    } else {
      // 如果是PC设备
      window.location.href = '/'
    }
    
  }

  const actLogout = () => {
    console.log('点击登出按钮')
    localStorage.removeItem(AUTH_TOKEN)
    console.log('aaa')
    window.location.href = '/login'
    console.log('aaa')
  }
  
  return {
    actLogin,
    actLogout,
  }
})