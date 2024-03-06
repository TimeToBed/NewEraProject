<template>
    <div class="user-info">
        <div class="user-form">
          <!-- form title -->
          <h6 class="text-xs text-muted py-1 -tracking-tighter uppercase mb-6 leading-6">
            考试名称：{{ userForm.examname }}
          </h6>
          <h6 class="text-xs text-muted py-1 -tracking-tighter uppercase mb-6 leading-6">
            考试科目： {{ userForm.subject }}
          </h6>
          <h6 class="text-xs text-muted py-1 -tracking-tighter uppercase mb-6 leading-6">
            考试时间： {{ userForm.time }}
          </h6>
          <div>
            
            <div class="flex justify-center mt-13.25">
              <el-button class="el-button--secondary" @click="lastForm">返回上一页</el-button>
              <el-button type="info">预览</el-button>
              <el-button type="success" @click="submit">发布</el-button>
            </div>
          </div>
        </div>
      </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, inject, reactive, ref} from 'vue'

  export default defineComponent({
    name: 'Finish',
    props: {
      examInfo:{
        type: Object,
        required: true
      }
    }, 
    emits:['back', 'submit'],
    setup(props, { emit }) {
      const formatDate = (data: Date) =>{
        const y = data.getFullYear();
        const m = ("0" + (data.getMonth() + 1)).slice(-2);  // 因为JavaScript的月份是从0开始算的，所以这里我们需要加一才能得到正确的月份
        const d = ("0" + data.getDate()).slice(-2);
        const h = ("0" + data.getHours()).slice(-2);
        const min = ("0" + data.getMinutes()).slice(-2); 
        const sec = ("0" + data.getSeconds()).slice(-2);
        return `${y}-${m}-${d} ${h}:${min}:${sec}`;  // 返回格式化的日期字符串
      };

      const userForm = ({
        examname: props.examInfo.examname,
        subject: props.examInfo.subject,
        time: formatDate(new Date(props.examInfo.time)),
      });

      const lastForm = () => {
        emit('back')
        console.log(userForm)
      }

      const submit = () => {
        emit('submit')

      }
      return {
        userForm, formatDate, lastForm, submit
      };
    },

  
  })
  </script>