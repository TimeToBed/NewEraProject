<template>
    <div class="w-full">
      <el-dialog title="上传试卷" :model-value.sync="dialogVisible" width="30%" :before-close="handleClose">
        <span>请按照上传文件格式上传：</span>
        <el-tree :data="data" :props="defaultProps" :default-expanded-keys="[3]" node-key="id"></el-tree>
        <br />
        <span slot="footer" class="dialog-footer">
          <div class="upload-actions">
            <input class="upload-demo" placeholder="上传试卷文件" type="file" @change="handleFolderUpload" webkitdirectory
              directory multiple>
            <el-button @click="closeDialog">取 消</el-button>
          </div>
          <!-- <div v-if="filesTree">
            <pre>{{ filesTree }}</pre>
          </div> -->
        </span>
      </el-dialog>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, inject, PropType, watch, ref, reactive } from 'vue'
  import { DotsVerticalIcon } from '@heroicons/vue/outline'
  import { AxiosInstance } from 'axios'
  import { ElMessageBox } from 'element-plus';
  import { componentSize } from 'element-plus/es/utils/props';

  
  export default defineComponent({
  
    name: 'UploadPapers',
    components: {
      DotsVerticalIcon,
    },
    props: {
        dialogVisible:{
            type: Boolean,
            required: true
        },
        exam_id:{
            type: Number,
            required: true
        }
    },
    data() {
      return {
        data: [{
          label: '总文件',
          children: [{
            label: '学生学号1',
            children: [{
              id: 3,
              label: '学生试卷照片1'
            },
            {
              id: 4,
              label: '学生试卷照片2'
            },
            {
              id: 5,
              label: '...'
            }]
          }, {
            label: '学生学号2',
            children: [{
              id: 3,
              label: '学生试卷照片1'
            },
            {
              id: 4,
              label: '学生试卷照片2'
            },
            {
              id: 5,
              label: '...'
            }]
          }, {
            label: '...',
          }
          ]
        }],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        filesTree: null,
      };
    },
    emits: ['update:dialogVisible', 'upload:upload'],
    setup(props, {emit}) {
        const axios = inject('axios') as AxiosInstance; // 确保你的项目中已经全局注册了 axios
        const filesTree = ref<any[]>([]);

        let dataToSend = reactive({
            get exam_id() {
                return props.exam_id
            },
            filelist: null,
        });

        const handleFolderUpload = async (event:any) => {
            console.log('dia:', props.dialogVisible)
            console.log('id:', props.exam_id)
            const files = event.target.files;
            let filelist = [];
            // 创建一个临时存储结构来容易地访问和更新文件列表
            let tempStorage = {};

            for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    if (file.type.startsWith('image/')) {
                    try {
                        const base64 = await image2file(file); // 异步获取文件的 Base64 编码
                        const parts = file.webkitRelativePath.split('/'); // 使用文件的相对路径
                        const filename = parts[parts.length - 2]; // 假设倒数第二部分是文件名

                        if (!tempStorage[filename]) {
                        tempStorage[filename] = { filename, file: [] };
                        filelist.push(tempStorage[filename]);
                        }
                        tempStorage[filename].file.push(base64); // 将 Base64 编码添加到对应的文件名下
                    } catch (error) {
                        console.error('Error converting file to base64:', error);
                    }
                    }
            }
            console.log('filelist:', filelist)

            filesTree.value = filelist; // 最终的文件列表结构
            postPaperData(filelist)
        }
        
        // 将图片文件转换为 Base64
        const fileToBase64 = (file: any) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => {
            resolve(e.target.result); // 返回 Base64 编码的字符串
            };
            reader.onerror = (e) => {
            reject(e);
            };
            reader.readAsDataURL(file); // 异步读取文件内容，结果用data:url的字符串形式表示
        });
        };

        const image2file = async (e: any) => {
        let base64 = await fileToBase64(e);
        return base64
        }


        // 提交文件
        const postPaperData =  async (e: any) => {
            dataToSend.filelist = e

            console.log('postpaperid:', dataToSend.exam_id)
            const response = await axios.post(`exams/uploadpapers/${dataToSend.exam_id}/`, dataToSend)
            .then((response) => {
                console.log('响应数据：', response.data);
                
                emit('update:dialogVisible', false);
                ElMessageBox.alert('上传成功！', '提示', {
                        confirmButtonText: '确定'
                      })
                emit('upload:upload', true)

            })
            .catch((error) => {
                console.error('请求错误：', error);
                ElMessageBox.alert('上传失败!', '警告', {
                        confirmButtonText: '确定'
                      })
            });
        };
        // 关闭上传框
        const handleClose = (done: () => void) => {
            ElMessageBox.confirm('确认关闭？')
                .then(_ => {
                    emit('update:dialogVisible', false);
                    done();
            })
                .catch(_ => {});
        };
        // 关闭上传框
        const closeDialog = () => {
            emit('update:dialogVisible', false);
        };


        // 控制台打印，证明 setup() 函数被调用
        console.log('create exam html');
  
        // 返回组件的响应式数据和方法，以便在模板中使用
        return {
            postPaperData, // 将 postPaperData 方法暴露给模板
            closeDialog,
            handleClose,
            handleFolderUpload,
            filesTree,
            fileToBase64,
            image2file

        };
    },
  });
  
  </script>
  
  <style scoped>
  .header-cell {
    text-align: center;
    font-weight: bold;
  }
  
  .upload-actions {
    display: flex;
    /* 启用Flexbox布局 */
    align-items: center;
    /* 垂直居中对齐子元素 */
    justify-content: space-between;
    /* 子元素之间保持平均间距 */
    gap: 10px;
    /* 设置子元素之间的间距 */
    width: 80%;
    margin: 0 10%;
  }
  
  .upload-demo,
  .el-button {
    flex: 1;
    /* 使两个元素各自占据一半的空间 */
    text-align: center;
    /* 若需要，可调整文本对齐方式 */
  }
  
  
  .upload-demo {
    flex-grow: 1;
    /* <input>元素会占据剩余空间 */
    height: 2.6875rem;
    background-color: #409eff;
    border: 1px solid #409eff;
    border-radius: 4px;
    padding: 7px 15px;
    font-size: .875rem;
    line-height: 1.5;
    font-weight: 600;
    letter-spacing: 0.025em;
    --tw-text-opacity: 1;
    color: #333;
    color: rgb(255 255 255 / var(--tw-text-opacity));
    cursor: pointer;
    box-sizing: border-box;
    --tw-border-opacity: 1;
    --tw-bg-opacity: 1;
    transition-property: all;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 100ms;
  }
  
  .upload-demo:hover {
    background-color: rgb(102, 177, 255);
  
    /* 鼠标悬停时的背景颜色 */
  
  }
  
  .cancel-demo {
    flex-grow: 1;
    height: 2.6875rem;
    border-width: 1px;
    --tw-border-opacity: 1;
    border-color: rgb(23 43 77 / var(--tw-border-opacity));
    --tw-bg-opacity: 1;
    background-color: rgb(23 43 77 / var(--tw-bg-opacity));
    font-size: .875rem;
    line-height: 1.5;
    font-weight: 600;
    letter-spacing: 0.025em;
    --tw-text-opacity: 1;
    color: rgb(255 255 255 / var(--tw-text-opacity));
    transition-property: all;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 100ms;
    flex-basis: 0;
  }
  </style>
  