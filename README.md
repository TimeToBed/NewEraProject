# Git仓库协作指南

本指南主要介绍如何从头开始在一个Git仓库进行协作以及遇到冲突时的处理方法。

## 开始使用Git仓库
1. **创建一个新的仓库**：因为我们已经有仓库所以不需要新建，只需要链接到项目仓库即可

2. **安装git**：window需要下载git客户端https://git-scm.com/downloads .之后可以在指定文件夹(比如你想要创建项目文件的地方)右键拉出选单，
   打开Open git bash here.你也可以在任意目录打开通过cd命令定位到某文件夹。

3. **连接到仓库前置 SSH 配置**：因为https的方式不稳定，所以我们统一用git的方式连接
   在git bash窗口输入命令:  
   创建昵称（随便起）  
   ` git config --global user.name "注册名"`  
   邮箱（你的github邮箱）  
   `git config --global user.email "注册邮箱"`  
   生成SSH Key  
   `ssh-keygen -t rsa -C "自己的邮箱"`  
   SSH文件存放在C:/User/用户/.ssh下，id_rsa为私钥，id_rsa.pub为公钥，用记事本打开公钥，其中内容为key（复制发我）
   打开 `C:/User/用户/.ssh/config` 在开头加入下方代码：  
   ```
   Host github.com
   User git
   Hostname ssh.github.com
   PreferredAuthentications publickey
   IdentityFile ~/.ssh/id_rsa
   Port 443
   ```

4. **克隆仓库**：验证ssh连接  
   `ssh -T git@github.com`
   使用`git clone [仓库的URL]`命令来克隆仓库到你的本地。  
   `git clone git@github.com:TimeToBed/NewEraProject.git`  
   进入工作区 `cd NewEraProject` （到这里一切都准备就绪了，bash会显示master标志）

6. **修改代码**：在你的本地对代码进行更改。

7. **提交更改**：更改完成后，使用`git add [文件名]`来添加更改，然后使用`git commit -m "这里写明修改的内容"`来提交你的更改。  
   `git add 单个文件`  
   `git add 文件1 文夹2 #……多个文件之间空格隔开`  
   `git add . #添加所有更改`
   提交前后使用`git status`查看状态是一个好习惯
8. **版本回退**：
   `git log`命令查看最近三次的提交`git reflog`查看更多次提交的信息  
   `git reset --hard HEAD^`回退到上一个版本`--hard HEAD^^`为回退到上上个版本，以此类推

9. **推送到远程仓库**：使用`git push`命令将你的更改推送到远程仓库(第一次需使用`git push -u origin master`)。origin为默认库名，master为默认分支名

## 如何解决冲突
如果你和你的协作者对同一份文件进行了不同的修改（比如在同一行），可能会发生冲突。下面是一些解决冲突的步骤：

1. **获取最新的代码**：使用 `git pull` 命令获取远程仓库的最新代码(第一次需使用`git pull origin master`)。
   
2. **查看冲突**：Git会提示你哪些文件存在冲突。

3. **解决冲突**：打开发生冲突的文件，找到Git标记的冲突部分（通常是以 `<<<<<<< HEAD` 开始，以 `>>>>>>> [commit ID]` 结束的部分），手动修改至你认为正确的状态。

4. **提交解决冲突后的文件**：解决冲突后，与之前的流程相同，使用 `git add [文件名]` 和 `git commit -m "your message"` 来提交你的更改。

5. **推送解决冲突后的代码**：使用`git push`命令把解决冲突后的代码推送到远程仓库。

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

## 项目运行

1. **运行后端项目**：在项目根目录下执行`python manage.py runserver`命令，打开浏览器访问http://127.0.0.1:8000/即可访问项目。
2. **运行前端项目**：在front目录下执行`npm run serve`命令，打开浏览器访问http://localhost:3000/即可访问项目。

## 最后
姐妹们记住，良好的沟通是预防和解决冲突的关键。如果能在修改代码之前与协作者讨论并告知他们你打算做什么，很多冲突都可以避免。

好的，姐妹们！

太牛了姐妹们！