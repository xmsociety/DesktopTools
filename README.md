# DesktopTools
    桌面端小工具

## 进度和计划
**进度和计划** 可在查看: [此处](https://github.com/IanVzs/Halahayawa/blob/dev/plan.md)

同时计划中包含了需求原型, 以及最一开始的代码实现原型, 有兴趣可以查看😄
# 功能介绍
## 工作时长统计
- 工作时长
- 按键记录
- 疲惫提醒-强制锁屏😄

## 粘贴板操作
- 时间转换
- 表格数据格式化
- dict json 格式化
- TODO
- 无限粘贴板
- 自定义kv存储


## 工作时长统计原理
检测鼠标以及键盘移动/输入,判断正在工作中.
macOS因隐私权限问题,需要额外设置,具体详参[此处](https://pynput.readthedocs.io/en/latest/limitations.html#macos)

### 实现
#### 编程语言
Python(不会卡的太死lol)

#### 所用库/包
- PyQt5: 实现简单界面(不想用其它包,卡的比较死^_^.....弃用,因为其授权协议问题,虽然我的是MIT不要紧,但是用了它我的协议就被升级...虽然PySide6也会升级本项目授权,但比PyQt5要好.)
- PySide6: 实现简单界面(不想用其它包,卡的不死^_^, 有MIT的实现方式欢迎改造)
- pynput: 监控鼠标键盘
- sqlalchemy: 数据库ORM,手拼字符累了,试试新东西
- yapf: 代码格式化 

# 使用
## PyPi
```bash
# 源码
git clone git@github.com:IanVzs/Halahayawa.git DesktopTools
cd DesktopTools/
make build
DesktopTools

# pypi
pip install DesktopTools[ui]
# 可选 -i https://pypi.tuna.tsinghua.edu.cn/simple
DesktopTools
```
## 源码
```bash
git clone git@github.com:IanVzs/Halahayawa.git DesktopTools
cd DesktopTools/
mkdir env
python3 -m venv ./env
source ~/env/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
make run # or python test.py
```

可根据实际情况进行适当调整
- `-i https://pypi.tuna.tsinghua.edu.cn/simple`是使用国内pip清华源, 如果有`timeout`的情况可自行搜索其他源来使用,或者不使用国内源`pip install -r requirements.txt`

## 可执行程序
### 下载地址
在[releases的Assets](https://github.com/IanVzs/Halahayawa/releases)中, 目前只上传了`windowsx64`版本。
### windows打包
`--icon`经测必须使用绝对路径.
```bash
pyinstaller --specpath=executable_files --distpath=executable_files --hidden-import=pynput.keyboard._xorg --hidden-import=pynput.mouse._xorg --hidden-import=sqlalchemy.sql.default_comparator --hidden-import=sqlalchemy.ext.baked --icon="C:\\Users\\{USERNAME}\\Desktop\\Halahayawa\\DesktopTools\\harry_potter.ico" -w -D --clean .\test.py
# cp harry_potter.ico executable_files/halahayawa 复制harry_potter.ico到程序目录
```
### linux打包
```
pyinstaller --specpath=executable_files --distpath=executable_files --hidden-import=pynput.keyboard._xorg --hidden-import=pynput.mouse._xorg --hidden-import=sqlalchemy.sql.default_comparator -w -D --clean test.py
```

# Poetry介绍
pip 管理
安装方式: `pip install poetry`

## 添加依赖
是的，Poetry提供了多种方式来自动添加依赖库。其中一种方式是使用命令`poetry add`，该命令允许您在不编辑`pyproject.toml`文件的情况下添加新的依赖项。例如，要添加`requests`包，版本为`^2.25.1`，可以运行以下命令：`poetry add requests "^2.25.1"`。这将会自动更新`pyproject.toml`文件并安装所需的依赖项。

另外，如果您已经安装了一个包，并且想要将其添加到项目中作为依赖项，可以使用`poetry add`命令并指定包的名称或路径。例如，要将已经安装的`numpy`包添加到项目中，可以运行以下命令：`poetry add numpy --dev`。这将在`pyproject.toml`文件中添加`numpy`作为开发依赖项，并更新虚拟环境以包含此包。

总之，Poetry提供了多种自动添加依赖项的方式，使得管理依赖项变得更加方便和高效。

### 手动添加依赖
要增加依赖库，可以按照以下步骤在`pyproject.toml`文件中进行：

1. 打开`pyproject.toml`文件。
2. 找到`[tool.poetry.dependencies]`部分，这是声明项目所需依赖的位置。
3. 在该部分下方添加一个新的依赖项，格式为`包名 = 版本号`。例如，如果要添加`requests`包，版本为`^2.25.1`，则可以将以下行添加到文件中：
  ```
  [tool.poetry.dependencies]
  requests = "^2.25.1"
  ```
4. 保存文件并关闭。

需要注意的是，当您添加新的依赖项时，Poetry会自动更新项目的虚拟环境以包含这些依赖项。因此，在添加新依赖后，请运行`poetry install`以更新项目的虚拟环境。