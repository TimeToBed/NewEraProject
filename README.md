

## 安装环境
python版本要求≥3.8

1. **安装Django**
   <pre>pip install django==3.2 -i https://pypi.douban.com/simple</pre>
2. **安装paddleocr**
   <pre>pip install paddlepaddle-gpu -i https://mirror.baidu.com/pypi/simple
   pip install paddleocr -i https://mirror.baidu.com/pypi/simple</pre>
3. **安装LLM SDK**
   <pre>pip install ./erniebot
   pip install ./erniebot-agent</pre>
4. **安装Vue环境和项目（前端开发需要安装）**
   ##### 安装nodejs（在项目环境中）
   <pre>conda install -c conda-forge nodejs</pre>
   ##### 查看是否安装成功
   <pre>node -v</pre>
   ##### 更换 nmp 源
   <pre>npm config set registry https://registry.npmmirror.com</pre>
   ##### 安装 vue-cli
   <pre>npm install -g @vue/cli</pre>
   ##### vue是否完全安装
   <pre>vue --version</pre>
   ##### 安装项目
   在front目录下执行`npm install`命令
   ##### 安装跨域库
   <pre>pip install django-cors-headers</pre>
5. **安装LLM外部知识库**
   ##### 安装langchain库等
   <pre>pip install langchain -U scikit-learn -U langchain-community spacy faiss-cpu</pre>
   ##### 安装本地whl
   <pre>pip install 你的路径/zh_core_web_sm-3.7.0-py3-none-any.whl（在群文件夹中）
6. **安装doc显示库**
   ##### 安装docx-preview（需要进入前端文件夹路径！！）
   <pre>npm i docx-preview --save</pre>
7. **安装轮播图的显示库**
    ##### 安装less (需要进入前端文件夹路径！！)
    <pre>npm install less --save-dev</pre>
    ##### 安装vue3-danmaku (需要进入前端文件夹路径！！)
    <pre>npm install vue3-danmaku</pre>

## 项目运行

1. **运行后端项目**：在项目根目录下执行`python manage.py runserver`命令，打开浏览器访问http://127.0.0.1:8000/即可访问项目。
2. **运行前端项目**：在front目录下执行`npm run serve`命令，打开浏览器访问http://localhost:3000/即可访问项目。

