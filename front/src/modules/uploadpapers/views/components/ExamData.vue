<template>
  <div class="w-full">
    <el-table :data="tableData" style="width: 100%" :class="`is-${theme}`" :cell-style="{ textAlign: 'center' }"
      :header-cell-style="{ textAlign: 'center' }">
      <el-table-column label="考试名称" min-width="200">
        <template #default="scope">
          <div class="px-4 cursor-auto">
            <span class="text-0.8125 font-normal">{{ scope.row.exam_name }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="考试时间" min-width="150">
        <template #default="scope">
          <div class="px-4 cursor-auto">
            <span class="text-0.8125 font-normal">{{ scope.row.exam_date }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="科目" min-width="150">
        <template #default="scope">
          <div class="px-4 flex items-center">
            <span class="ml-2 pb-0.5 text-0.875 font-normal">{{ scope.row.subject }}</span>
          </div>
        </template>
      </el-table-column>

      <el-table-column min-width="100">
        <template #default="scope">
          <el-button type="primary" size="large" @click="handleButtonClickUpload(scope.row)">上传试卷</el-button>
        </template>
      </el-table-column>

      <el-table-column min-width="100">
        <template #default="scope">
          <el-button :type="getButtonType(scope.row.ismarking)" :class="getButtonClass(scope.row.ismarking)"
            :disabled="isButtonDisabled(scope.row.ismarking)" size="large" @click="handleButtonClickMarking(scope.row)">
            批改试卷
          </el-button>
        </template>
      </el-table-column>

      <el-table-column width="60" fixed="right">
        <div class="text-center h-12 pt-2.5">
          <el-dropdown placement="bottom-end" trigger="click" popper-class="action-column-popper">
            <el-button class="w-5 h-7 border-none bg-transparent hover:shadow-md" plain>
              <div class="flex items-center space-x-2 2xl:space-x-4 text-black px-5">
                <DotsVerticalIcon class="cursor-pointer h-5 w-5 text-[#ced4da] font-extrabold" />
              </div>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu class="my-0.5">
                <el-dropdown-item class="mx-0 hover:bg-secondary text-zinc-800">
                  <div class="flex items-center w-40 h-6">
                    <span class="mb-0 text-sm font-normal">Action</span>
                  </div>
                </el-dropdown-item>

                <el-dropdown-item class="mx-0 hover:bg-secondary text-zinc-800">
                  <div class="flex items-center w-40 h-6">
                    <span class="mb-0 text-sm font-normal">Another Action</span>
                  </div>
                </el-dropdown-item>

                <el-dropdown-item class="mx-0 hover:bg-secondary text-zinc-800">
                  <div class="flex items-center w-40 h-6">
                    <span class="mb-0 text-sm font-normal">Something else here</span>
                  </div>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-table-column>
    </el-table>
    <el-dialog title="上传试卷" :model-value.sync="dialogVisible" width="30%" :before-close="handleClose">
      <span>请按照上传文件格式上传：</span>
      <el-tree :data="data" :props="defaultProps" :default-expanded-keys="[3]" node-key="id"></el-tree>
      <br />
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <input class="upload-demo" placeholder="上传试卷文件" type="file" @change="handleFolderUpload" webkitdirectory directory multiple>
        <!-- <el-upload class="upload-demo" action="handleFolderUpload" :file-list="fileList">
          <el-button size="small" type="primary">点击上传</el-button>
        </el-upload> -->
        <div v-if="filesTree">
          <pre>{{ filesTree }}</pre>
        </div>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { DotsVerticalIcon } from '@heroicons/vue/outline'

export default defineComponent({

  name: 'ExamData',
  components: {
    DotsVerticalIcon,
  },
  data() {
    return {
      dialogVisible: false,
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
  props: {
    tableData: {
      type: Array,
      required: true,
    },
    theme: {
      type: String,
      required: false,
      default: 'light',
    },
  },
  methods: {
    handleButtonClickUpload(row) {
      this.dialogVisible = true
      console.log(this.dialogVisible)
    },
    handleButtonClickMarking(row) {
      console.log('批改试卷', row)
      this.$router.push('/marking/marking_papers');
    },
    getButtonType(ismarking) {
      return ismarking ? 'primary' : '';
    },
    getButtonClass(ismarking) {
      return ismarking ? '' : 'el-button--secondary';
    },
    isButtonDisabled(ismarking) {
      return !ismarking;
    },
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done();
        })
        .catch(_ => { });
    },
    handleFolderUpload(event) {
      const files = event.target.files;
      let structure = {};

      for (let i = 0; i < files.length; i++) {
        const path = files[i].webkitRelativePath;
        let parts = path.split('/');
        parts.reduce((acc, current, index) => {
          if (!acc[current]) {
            acc[current] = index === parts.length - 1 ? files[i] : {};
          }
          return acc[current];
        }, structure);
      }

      this.filesTree = JSON.stringify(structure, null, 2);
    },
  }
})
</script>
  
<style scoped>
.header-cell {
  text-align: center;
  font-weight: bold;
}
</style>
