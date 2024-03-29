<template>
  <div class="w-full">
    <el-card class="bg-secondary text-center pb-6">
      <!-- <template #header>
        <div class="text-muted text-center mt-2 mb-4">
          <small class="text-90">请选择身份</small>
        </div>
        <div class="pb-6 flex flex-nowrap text-center justify-center">
          <el-button class="bg-white border-white" href="#">
            <img src="@/assets/images/github.png" alt="" class="h-4 w-4" />
            <span class="pl-4 text-indigo-410">老师</span>
          </el-button>
          <el-button class="bg-white border-white" href="#">
            <img src="@/assets/images/google.png" alt="" class="h-4 w-4" />
            <span class="pl-4 text-indigo-410">学生</span>
          </el-button>
        </div>
      </template> -->
      <div class="content-center items-center w-full lg:p-6">
        <div class="mb-4 mt-2 text-center">
          <small class="block w-full text-12.8 mb-6 text-muted">{{ description }}</small>
        </div>
        <el-form ref="form" :model="formData" class="authentication-form">
          <el-form-item class="warning-input mb-4 rounded-md" prop="email">
            <el-radio-group v-model="formData.usertype" >
              <el-radio label="1" size="large">教师</el-radio>
              <el-radio label="2" size="large">学生</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item class="warning-input mb-4 rounded-md" prop="email">
            <div class="z-10 absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <div class="w-5 h-5">
                <MailIcon class="w-5 h-5 text-gray-210" />
              </div>
            </div>
            <el-input placeholder="Email" v-model="formData.email" />
          </el-form-item>
          <el-form-item class="mb-6 rounded-md" prop="password">
            <div class="z-10 absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <div class="w-5 h-5">
                <LockOpenIcon class="w-5 h-5 text-gray-210" />
              </div>
            </div>
            <el-input type="password" placeholder="Password" v-model="formData.password" />
          </el-form-item>
          <el-form-item class="mb-4">
            <el-checkbox class="text-muted font-normal">Remember me</el-checkbox>
          </el-form-item>
        </el-form>
        <el-button type="primary" @click="handleLoginClick"> Sign in </el-button>
      </div>
    </el-card>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, inject, h } from 'vue'
import useStore from 'store'
import { MailIcon, LockOpenIcon } from '@heroicons/vue/solid'
import { ElNotification } from 'element-plus';
import { AxiosInstance } from 'axios';


export default defineComponent({
  name: 'LoginForm',
  components: {
    MailIcon,
    LockOpenIcon,
  },
  props: {
    height: {
      type: Number,
    },
    description: {
      type: String,
      default: '',
    },
    email: {
      type: String,
      default: '',
    },
    password: {
      type: String,
      default: '',
    },
    usertype :{
      type: String,
      default: '1'
    }
  },
  setup(props) {
    const store = useStore()
    const form = ref<ElementForm>()
    const formData = ref({ email: props.email, password: props.password, usertype: props.usertype })
    const axios = inject('axios') as AxiosInstance
    const handleKeyDown = async () => {
      login()
    }

    const handleLoginClick = async () => {
      login()
    }

    const login = async () => {
      try {
        if (!store.auth.isAuthenticated) {
          console.log('登录------------------', formData.value)
          let form=new FormData()
          form.append('email',formData.value.email)
          form.append('password',formData.value.password)
          form.append('usertype', formData.value.usertype)
          const response = await axios.post('exams/login/', form)
          .then(function (response) {
                      console.log(response);
                      if (response.data.result=='登录成功'){
                        ElNotification({
                          title: '提示',
                          message: h('i', { style: 'color: teal' }, '登录成功！'),
                          type: 'success'
                        })
                        let teacher_id=response.data.teacher_id
                        let username=response.data.username
                        localStorage.setItem('user_id', teacher_id) 
                        localStorage.setItem('username', username) 
                        store.auth.actLogin(formData.value)
                      }else if (response.data.result=='用户名不存在'){
                        ElNotification({
                          title: '提示',
                          message: h('i', { style: 'color: teal' }, '用户名不存在！'),
                          type: 'warning'
                        })
                      }else if (response.data.result=='密码错误'){
                        ElNotification({
                          title: '提示',
                          message: h('i', { style: 'color: teal' }, '密码错误！'),
                          type: 'error'
                        })
                      }
                    })
                    .catch(function (error) {
                      console.log(error);
                    });
          

        }
      } catch (e) {
        console.log('err::: ', e)
      }
    }
    return {
      form,
      formData,
      handleLoginClick,
      handleKeyDown,
    }
  },
})
</script>
