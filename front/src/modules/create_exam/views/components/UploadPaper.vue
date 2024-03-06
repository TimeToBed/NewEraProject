<template>
  <div class="user-info">
        <div class="user-form">
          <!-- form title -->
          <h6 class="text-xs text-muted py-1 -tracking-tighter uppercase mb-6 leading-6">
            请选择本次考试的样题和答案进行上传！
          </h6>
          <div>
            <el-form :model="userForm.paper" label-position="top">
              <el-form-item label="上传样题">
                <el-upload class="w-full" action="#" :auto-upload="false" 
                @change="handlePaperChange">
                  <el-input placeholder="考题.word" class="input-upload">
                    <template #append>浏览</template>
                  </el-input>
                </el-upload>
              </el-form-item>
            </el-form>
            <el-form :model="userForm.result" label-position="top">
              <el-form-item label="上传答案(可选)">
                <el-upload class="w-full" action="#" :auto-upload="false" 
                @change="handleResultChange">
                  <el-input placeholder="答案.word" class="input-upload">
                    <template #append>浏览</template>
                  </el-input>
                </el-upload>
              </el-form-item>
            </el-form>
            <div class="flex justify-center mt-13.25">
              <el-button class="el-button--secondary" @click="lastForm">返回上一页</el-button>
              <el-button type="success" @click="nextForm">保存并进入下一页</el-button>
            </div>
          </div>
        </div>
      </div>
</template>
<script lang="ts">
import { defineComponent, reactive, ref } from 'vue'

export default defineComponent({
  name: 'UploadPaper',
  props: {
    examInfo:{
      type: Object,
      required: true
    }
  },
  emits:['continue', 'back'],
  setup(props, {emit}) {
    const userForm = reactive({
      paper: props.examInfo.paper,
      result: props.examInfo.result,
    })

    const handlePaperChange = (file: any) => {
      userForm.paper = file;
      console.log(userForm.paper)
      console.log('得到试卷文件')
    }
    
    const handleResultChange = (file: any) => {
      userForm.result = file;
      console.log('得到答案文件')
    }

    const nextForm = () => {
      Object.assign(props.examInfo, userForm)
      emit('continue')
    }

    const lastForm = () => {
      emit('back')
    }

    return {
      userForm, nextForm, lastForm, handlePaperChange, handleResultChange
    }
  },
})
</script>
