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
            <div class="flex justify-center items-center h-full">
              <img v-if="currentStep === 4" src="../../../../assets/images/yes.gif" class="w-24 h-24" />
            </div>
            
            <div class="flex justify-center">
              <el-button v-if = "currentStep === 3" class="el-button--secondary" @click="lastForm">返回上一页</el-button>
              <el-button v-if = "currentStep === 4" type="success" @click="reset">继续创建</el-button>
              <el-button v-if = "currentStep === 4" type="info" @click="handleButtonClickUpload">上传试卷</el-button>
              <UploadPapers :dialogVisible.sync="dialogVisible" :exam_id="exam_id"
              @update:dialogVisible="updateDialogVisible"></UploadPapers>
              <el-button v-if = "currentStep === 3" type="success" @click="submit">发布</el-button>
            </div>
          </div>
        </div>
      </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, inject, watch, reactive, ref} from 'vue'
  import { AxiosInstance } from 'axios'
  import UploadPapers from '../../../uploadpapers/views/components/UploadPapers.vue'

  export default defineComponent({
    name: 'Finish',
    props: {
      examInfo:{
        type: Object,
        required: true
      },
      currentStep:{
        required: true
      }
    }, 
    components:{
      UploadPapers
    },
    emits:['back', 'submit', 'continue', 'reset-currentStep', 'reset-examInfo'],
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

      const currentStep = ref(props.currentStep)
      console.log("currentStep: ", currentStep)

      const userForm = ({
        examname: props.examInfo.examname,
        subject: props.examInfo.subject,
        time: formatDate(new Date(props.examInfo.time)),
      });
      
      const lastForm = () => {
        emit('back')
        console.log(userForm)
      }
      const reset = () => {
        emit('reset-currentStep', 1);
        emit('reset-examInfo');
      }

      const submit = () => {
        emit('submit')
        emit('continue')

      }

      const state = reactive({  //  Vue 的响应性 API，当我们改变这个数据时，Vue 能知道需要重新渲染影响的组件。
      exam: null,
      tableLoading: false,
      CurrentPage: 1,
      PageSize: 10,
      Total: 0,
      tableData:[],
      })

      // 所选考试的id
      const exam_id = ref(0);

      const dialogVisible = ref(false);

      watch(dialogVisible, (newValue, oldValue) => {
        console.log('dialogVisible 变化了, 旧值: ', oldValue, ', 新值: ', newValue);
      });

      const handleButtonClickUpload = () => {
        dialogVisible.value = true
        // console.log('dialogVisible:', dialogVisible.value)
        exam_id.value = props.examInfo.exam_id // 对应到所选考试的exam_id
        // console.log('exam_id:', exam_id.value)
      };

      const updateDialogVisible = (newValue: boolean) => {
        dialogVisible.value = newValue
      };

      // 控制台打印，证明 setup() 函数被调用
      console.log('create exam html');
      


      return {
        userForm, formatDate, lastForm, submit, reset, state,
        handleButtonClickUpload, updateDialogVisible, dialogVisible, exam_id
      };
    },

  
  })
  </script>