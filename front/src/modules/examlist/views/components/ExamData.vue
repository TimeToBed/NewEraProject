<template>
    <div class="w-full">
      <el-table 
      :data="tableData" 
      style="width: 100%" 
      :class="`is-${theme}`" 
      :cell-style="{ textAlign: 'center' }"
      :header-cell-style="{ textAlign: 'center' }">
        <el-table-column label="序号" min-width="60" >
          <template #default="scope">
            <div class="px-4 cursor-auto">
              <span class="text-0.8125 font-normal">{{ scope.row.index }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="考试名称" min-width="200" >
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
        <el-table-column label="科目" min-width="120">
          <template #default="scope">
            <div class="px-4 cursor-auto">
              <span class="text-0.875 font-normal">{{ scope.row.subject }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column min-width="80">
          <template #default="scope">
            <el-button  type="primary" size="large" @click="handleButtonClickUpload(scope.row)">上传试卷</el-button>
          </template>
        </el-table-column>

        <el-table-column min-width="80">
          <template #default="scope">
            <el-button
              :type="getButtonType(scope.row.markingable)"
              :class="getButtonClass(scope.row.markingable)"
              :disabled="isButtonDisabled(scope.row.markingable)"
              size="large" 
              @click="handleButtonClickMarking(scope.row)">
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
    </div>
  </template>
  <script lang="ts">
  import { defineComponent } from 'vue'
  import { DotsVerticalIcon } from '@heroicons/vue/outline'
  
  export default defineComponent({
    
    name: 'ExamData',
    components: {
      DotsVerticalIcon,
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
        console.log('上传试卷',row)
        this.$router.push('/marking/upload_papers');
      },
      handleButtonClickMarking(row) {
        console.log('批改试卷',row)
        //this.$router.push({ path: '/marking/marking_papers', query: { id: row.exam_id } });
        this.$router.push({ path: '/paperlist', query: { exam_id: row.exam_id } });
      },
      getButtonType(markingable) {
        return markingable ? 'primary' : '';
      },
      getButtonClass(markingable) {
        return markingable ? '' : 'el-button--secondary';
      },
      isButtonDisabled(markingable) {
        return !markingable;
      }
    },
  })
  </script>
  
<style scoped>

.header-cell {
  text-align: center;
  font-weight: bold;
}

</style>