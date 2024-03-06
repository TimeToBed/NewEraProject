<template>
    <div class="w-full">
      <el-table 
      :data="tableData" 
      style="width: 100%" 
      :class="`is-${theme}`" 
      :cell-style="{ textAlign: 'center' }"
      :header-cell-style="{ textAlign: 'center' }">
        <el-table-column label="考生学号" min-width="200" >
          <template #default="scope">
            <div class="px-4 cursor-auto">
              <span class="text-0.8125 font-normal">{{ scope.row.student_id }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="考生姓名" min-width="150">
          <template #default="scope">
            <div class="px-4 cursor-auto">
              <span class="text-0.8125 font-normal">{{ scope.row.student_name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="页数" min-width="150">
          <template #default="scope">
            <div class="px-4 cursor-auto">
              <span class="text-0.8125 font-normal">{{ scope.row.pages }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="状态" min-width="167">
          <template #default="scope">
            <div class="px-4 cursor-auto flex items-center">
              <i
                class="w-2 h-2 rounded-full ml-14"
                aria-hidden="true"
                :class="[
                  scope.row.state == 2
                    ? 'bg-info'
                    : scope.row.state == 0
                    ? 'bg-danger'
                    : scope.row.state == 1
                    ? 'bg-warning'
                    : 'bg-success',
                ]"
              ></i>
              <!-- <span class="ml-2 pb-0.5 text-0.875 font-normal">{{ scope.row.state }}</span> -->
              <span class="ml-4 pb-0.5 text-0.875 font-normal"
              v-if="scope.row.state==0">未批改</span>
              <span class="ml-4 pb-0.5 text-0.875 font-normal"
              v-if="scope.row.state==1">批改中</span>
              <span class="ml-4 pb-0.5 text-0.875 font-normal"
              v-if="scope.row.state==2">批改完</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column min-width="100">
          <template #default="scope">
            <el-button  type="primary" size="large" @click="handleButtonClickMarking(scope.row)">批改试卷</el-button>
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
  import { defineComponent, ref } from 'vue'
  import { DotsVerticalIcon } from '@heroicons/vue/outline'
  
  export default defineComponent({
    
    name: 'PaperData',
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
      handleButtonClickMarking(row) {
        console.log('批改试卷',row)
        this.$router.push('/marking/marking_papers');
      },
    },
    setup () {
      const theme = ref([
        { status: 'on schedule', color: '#11CDEF' },
        { status: 'delayed', color: '#F5365C' },
        { status: 'pending', color: '#FB6340' },
      ])
      const customColorMethod = (status: string) => {
        return theme.value.find((el: any) => el.status == status)?.color ?? '#2DCE89'
      }
      return {
        customColorMethod,
      }
    }
  })
  </script>
  
<style scoped>

.header-cell {
  text-align: center;
  font-weight: bold;
}

</style>