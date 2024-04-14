import {
  HomeIcon,
  ColorSwatchIcon,
  CursorClickIcon,
  DocumentReportIcon,
  DesktopComputerIcon,
  CloudUploadIcon,
  PencilIcon,
  TrendingUpIcon,
  SunIcon,
  UserCircleIcon,
  UsersIcon,
  ViewGridAddIcon,
  DocumentTextIcon,
  ViewBoardsIcon,
  BellIcon,
  LocationMarkerIcon,
  UserIcon,
  ViewGridIcon,
  StarIcon,
  LightBulbIcon
} from '@heroicons/vue/outline'

import {
  CreditCardIcon,
} from '@heroicons/vue/solid'



const Login = () => import('modules/auth/views/login.vue')
const Register = () => import('modules/auth/views/register.vue')
const ForgotPassword = () => import('modules/auth/views/forgot-password.vue')
const NotFound = () => import('modules/pages/views/404.vue')
const Dashboard = () => import('modules/dashboard/views/index.vue')
const Table = () => import('modules/table/views/index.vue')
const Grid = () => import('modules/grid/views/index.vue')
const Notification = () => import('modules/notification/views/index.vue')
const Button = () => import('modules/buttons/views/index.vue')
const Typography = () => import('modules/typography/views/index.vue')
const Card = () => import('modules/cards/views/index.vue')
const Icons = () => import('modules/icons/views/index.vue')
const Profile = () => import('modules/profile/views/index.vue')
const Map = () => import('modules/map/views/index.vue')
const ExamList = () => import('modules/examlist/views/index.vue')
const PaperList = () => import('modules/paperlist/views/index.vue')
const CreateExam = () => import('modules/create_exam/views/index.vue')
const UploadPapers = () => import('modules/uploadpapers/views/index.vue')
const MarkingPapers = () => import('modules/markingpapers/views/index.vue')
const MarkingPaper = () => import('modules/markingpaper/views/index.vue')
const PreviewLLM = () => import('modules/previewLLM/views/index.vue')
const Fake = () => import('modules/fake/views/index.vue')
const GrowUp = () => import('modules/growup/views/index.vue')

const ComponentLayout = () => import('components/ComponentLayout/index.vue')
const ExamLayout = () => import('components/ExamLayout/index.vue')
const MarkingLayout = () => import('components/MarkingLayout/index.vue')
const Students = () => import('modules/students/views/index.vue')

const routes = [
  /*移动端的页面   目前只让进主页(即学情分析)*/
  {
    path: '/login',
    component: Login,
    name: 'login',
    meta: {
      requiresAuth: false,
      isMobile: true,
    },
  },
  {
    path: '/students',
    component: Students,
    name: 'Students',
    meta: {
      title: '学生端',
      isMobile: true,
      requiresAuth: true,
    }
  },
  /*PC端的页面 */
  {
    path: '/',
    component: Dashboard,
    name: 'Dashboard',
    meta: {
      title: '首页',
      icon: HomeIcon,
      color: 'text-indigo-410',
      requiresAuth: true,
      parentPath: 'Home',
      isMobile: false
    },
  },
  {
    path: '/exam',
    component: ExamLayout,
    name: 'Exam',
    meta: {
      title: '考试',
      icon: ColorSwatchIcon,
      color: 'text-info',
      requiresAuth: true,
      parentPath: 'Home',
      isMobile: false
    },
    children: [
      {
        path: 'create_exam',
        name: 'CreateExam',
        component: CreateExam,
        meta: {
          title: '创建考试',
          icon: CursorClickIcon,
          color: 'text-danger-50',
          requiresAuth: true,
        },
      },
      {
        path: 'examlist',
        name: 'ExamList',
        component: ExamList,
        meta: {
          title: '查看已有考试',
          icon: DocumentReportIcon,
          color: 'text-success-50',
          requiresAuth: true,
        },
      },
    ]
  },
  // {
  //   path: '/paperlist',
  //   component: Profile,
  // },
  {
    path: '/marking',
    component: MarkingLayout,
    name: 'MarkingLayout',
    meta: {
      title: '阅卷',
      icon: DesktopComputerIcon,
      color: 'text-warning-50',
      requiresAuth: true,
      parentPath: 'Home'
    },
    children: [
      {
        path: 'upload_papers',
        name: 'UploadPapers',
        component: UploadPapers,
        meta: {
          title: '上传试卷',
          icon: CloudUploadIcon,
          color: 'text-danger-50',
          requiresAuth: true,
        },
      },
      {
        path: 'marking_papers',
        component: MarkingPapers,
        name: 'MarkingPapers',
        meta: {
          title: '批改试卷',
          icon: PencilIcon,
          color: 'text-success-50',
          requiresAuth: true,
        },
      },
    ]
  },

  {
    path: '/components/:componentItem?',
    component: ComponentLayout,
    name: 'Components',
    meta: {
      title: '学情分析',
      icon: TrendingUpIcon,
      color: 'text-yellow-310',
      requiresAuth: true,
      parentPath: 'Components'
    },
    children: [
      {
        path: 'buttons',
        name: 'Buttons',
        component: Button,
        meta: {
          title: '待定',
          icon: SunIcon,
          color: 'text-danger-50',
          requiresAuth: true,
        },
      },
    ]
  },
  {
    path: '/growup',
    component: GrowUp,
    name: 'GrowUp',
    meta: {
      title: '智能成长',
      icon: LightBulbIcon,
      color: 'text-success-50',
      requiresAuth: true,
      parentPath: 'Home'
    },
  },

  {
    path: '/components/:componentItem?',
    component: ComponentLayout,
    name: 'Components',
    meta: {
      title: '人员',
      icon: UserCircleIcon,
      color: 'text-indigo-410',
      requiresAuth: true,
      parentPath: 'Components'
    },
    children: [
      {
        path: 'buttons',
        name: 'Buttons',
        component: Button,
        meta: {
          title: '考生列表',
          icon: UsersIcon,
          color: 'text-danger-50',
          requiresAuth: true,
        },
      },
    ]
  },
  {
    path: '/components/:componentItem?',
    component: ComponentLayout,
    name: 'Components',
    meta: {
      title: '更多',
      icon: ViewGridAddIcon,
      color: 'text-info',
      requiresAuth: true,
      parentPath: 'Components'
    },
    children: [
      {
        path: 'buttons',
        name: 'Buttons',
        component: Button,
        meta: {
          title: '待定',
          icon: CursorClickIcon,
          color: 'text-danger-50',
          requiresAuth: true,
        },
      },
    ]
  },
  {
    path: '/fake',
    component: Fake,
    name: 'Fake',
    meta: {
      requiresAuth: true,
    },
  },

  
  {
    path: '/register',
    component: Register,
    name: 'Register',
    meta: {
      requiresAuth: false,
    },
  },

  {
    path: '/components/:componentItem?',
    component: ComponentLayout,
    name: 'Components',
    meta: {
      title: 'Components',
      //icon: ColorSwatchIcon,
      color: 'text-info',
      requiresAuth: true,
      parentPath: 'Components'
    },
    children: [
      {
        path: 'buttons',
        name: 'Buttons',
        component: Button,
        meta: {
          title: 'Buttons',
          icon: CursorClickIcon,
          color: 'text-danger-50',
          requiresAuth: true,
        },
      },
      {
        path: 'notifications',
        component: Notification,
        name: 'Notifications',
        meta: {
          title: 'Notifications',
          icon: BellIcon,
          color: 'text-success-50',
          requiresAuth: true,
        },
      },
      {
        path: 'tables',
        component: Table,
        name: 'Tables',
        meta: {
          title: 'Tables',
          icon: ViewBoardsIcon,
          color: 'text-indigo-410',
          requiresAuth: true,
        },
      },
      {
        path: 'grid',
        component: Grid,
        name: 'Grid',
        meta: {
          title: 'Grid',
          icon: ViewGridIcon,
          color: 'text-info',
          requiresAuth: true,
        },
      },
      {
        path: 'typography',
        component: Typography,
        name: 'Typography',
        meta: {
          title: 'Typography',
          icon: DocumentTextIcon,
          color: 'text-yellow-310',
          requiresAuth: true,
        },
      },
      {
        path: 'cards',
        component: Card,
        name: 'Cards',
        meta: {
          title: 'Cards',
          icon: CreditCardIcon,
          color: 'text-warning-50',
          requiresAuth: true,
        },
      },
      {
        path: 'icons',
        component: Icons,
        name: 'Icons',
        meta: {
          title: 'Icons',
          icon: StarIcon,
          color: 'text-red-410',
          requiresAuth: true,
        },
      },
    ]
  },
  // {
  //   path: '/profile',
  //   component: Profile,
  //   name: 'Profile',
  //   meta: {
  //     title: 'Profile',
  //     icon: UserIcon,
  //     color: 'text-success-50',
  //     isDarkBackground: true,
  //     isFullWidthLayout: true,
  //     requiresAuth: true,
  //     parentPath: 'Home'
  //   },
  // },
  // {
  //   path: '/map',
  //   component: Map,
  //   name: 'Map',
  //   meta: {
  //     title: 'Map',
  //     icon: LocationMarkerIcon,
  //     color: 'text-red-410',
  //     requiresAuth: true,
  //     parentPath: 'Home'
  //   },
  // },
  {
    path: '/paperlist',
    component: PaperList,
    name: 'PaperList',
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/marking_paper',
    component: MarkingPaper,
    name: 'MarkingPaper',
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/previewllm',
    component: PreviewLLM,
    name: 'PreviewLLM',
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/forgot-password',
    component: ForgotPassword,
    name: 'forgot-password',
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: '/:pathMatch(.*)*',
    component: NotFound,
    name: 'NotFound',
    meta: {
      requiresAuth: false,
    },
  },
]

export default routes
