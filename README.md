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
