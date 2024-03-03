<template>
  <div class="user-info">
    <div class="user-form">
      <!-- form title -->
      <h6 class="text-xs text-muted py-1 -tracking-tighter uppercase mb-6 leading-6">
        请按照规则填写本场考试的基本信息：
      </h6>
      <h6 class="text-xs text-muted py-1 -tracking-tighter uppercase mb-6 leading-6">
        考试标题如：2023-2024语文第一次期末考试；
        考试科目如：语文
      </h6>
      <div>
        <el-form :model="userForm" label-position="top">
          <el-form-item label="考试标题">
            <el-input v-model="userForm.examname" placeholder="最多可填写40个字符(汉字占两个字符)" @blur="isTouchedExamTitle=true"/>
            <div v-if="isTouchedExamTitle && isEmptyExamname" class="text-red-500 text-sm">{{ messageExamname }}</div>
          </el-form-item>
          <el-form-item label="考试科目">
            <el-input v-model="userForm.subject" placeholder="最多可填写20个字符(汉字占两个字符)" @blur="isTouchedSubject=true"/>
            <div v-if="isTouchedSubject && isEmptySubject" class="text-red-500 text-sm">{{ messageSubject }}</div>
          </el-form-item>

          <el-form-item label="考试时间">
            <el-date-picker
              v-model="userForm.time"
              type="datetime"
              placeholder="选择日期时间"
              @blur="isTouchedTime=true"
              >
            </el-date-picker>
            <div v-if="isTouchedTime && isEmptyTime" class="text-red-500 text-sm">{{ messageTime }}</div>
          </el-form-item>
        </el-form>
        <div class="flex justify-center mt-13.25">
          <el-button type="success" @click="nextForm">保存并进入下一页</el-button>
        </div>
      </div>
    </div>
  </div>

</template>

<script lang="ts">

import { defineComponent, reactive, ref, watch } from 'vue'

export default defineComponent({
  name: 'BasicInfo',
  props:{
    examInfo:{
      type: Object,
      required: true
    }
  },
  emits:['continue'],
  setup(props, {emit}) {
    const userForm = reactive({
      examname: props.examInfo.examname,
      subject: props.examInfo.subject,
      time: props.examInfo.time,
    })

    const isTouchedExamTitle = ref(false);
    const isTouchedSubject = ref(false);
    const isTouchedTime = ref(false);

    const isEmptyExamname = ref(false);
    const messageExamname = ref('');

    const isEmptySubject = ref(false);
    const messageSubject = ref('');

    const isEmptyTime = ref(false);
    const messageTime = ref('');

    watch(userForm, (newVal) => {
        isTouchedExamTitle.value && (isEmptyExamname.value = !newVal.examname.trim());
        isTouchedSubject.value && (isEmptySubject.value = !newVal.subject.trim());
        isTouchedTime.value &&  (isEmptyTime.value = !newVal.time);
        messageExamname.value = isEmptyExamname.value ? '请填写考试标题' : '';
        messageSubject.value = isEmptySubject.value ? '请填写考试科目' : '';
        messageTime.value = isEmptyTime.value ? '请选择考试时间' : '';
    },{ deep: true });

    const nextForm = () => {
      if (userForm.examname && userForm.subject && userForm.time) {
        Object.assign(props.examInfo, userForm)
        emit('continue')
        console.log(userForm)
      } else{
        console.log('有必填信息未填写！')
      }
    }



    return {
      userForm, nextForm,
      isTouchedExamTitle,
      isTouchedSubject,
      isTouchedTime,
      isEmptyExamname,
      isEmptySubject,
      isEmptyTime,
      messageExamname,
      messageSubject,
      messageTime
    }
  },
})
</script>
