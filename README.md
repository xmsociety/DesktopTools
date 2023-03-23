# DesktopTools
桌面端小工具

## 进度和计划
进度和计划: 可在查看[此处](https://github.com/IanVzs/Halahayawa/blob/dev/plan.md)

## 使用
### 源码
```bash
git clone git@github.com:IanVzs/Halahayawa.git DesktopTools
cd DesktopTools/
mkdir env
python3 -m venv ./env
source ~/env/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
python main.py
```

可根据实际情况进行适当调整
- `-i https://pypi.tuna.tsinghua.edu.cn/simple`是使用国内pip清华源, 如果有`timeout`的情况可自行搜索其他源来使用,或者不使用国内源`pip install -r requirements.txt`

### 可执行程序
#### 下载地址
在[releases的Assets](https://github.com/IanVzs/Halahayawa/releases)中, 目前只上传了`windowsx64`版本。
#### windows
`--icon`经测必须使用绝对路径.
```bash
pyinstaller --specpath=executable_files --distpath=executable_files --hidden-import=pynput.keyboard._xorg --hidden-import=pynput.mouse._xorg --hidden-import=sqlalchemy.sql.default_comparator --hidden-import=sqlalchemy.ext.baked --icon="C:\\Users\\USERNAME\\Desktop\\Halahayawa\\harry_potter.ico" -w -D --clean halahayawa.py
# cp harry_potter.ico executable_files/halahayawa 复制harry_potter.ico到程序目录
```
#### linux
```
pyinstaller --specpath=executable_files --distpath=executable_files --hidden-import=pynput.keyboard._xorg --hidden-import=pynput.mouse._xorg --hidden-import=sqlalchemy.sql.default_comparator -w -D --clean halahayawa.py
```


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
##### yapf
查看工具格式将修改哪些地方 和 应用修改, 配置文件`.style.yapf`
```bash
python3 -m yapf . -d -r
python3 -m yapf . -i -r
```
如果代码中某一段不想用yapf格式化
```python
# yapf: disable
a = {
    "666": "999",
    "999": "666"
}
mat = [
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5]
]
# yapf: enable
```
或
```python
mat = [
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5]
] # yapf: disable
```


## 包含信息
- [x] 当前单次连续工作时长 历史最大/最小
- [ ] 当前单日工作总时长 历史最大/最小
- [ ] 当前单周总工作时长 历史最大/最小
- [ ] 当前单月总工作时长 历史最大/最小
- [ ] 跨度: 天/周/月/年数
- [x] 展示当前单次连续工作时长
- [x] 展示单次运行工作总时长
- [ ] 展示以上其余信息

## 中断机制
- [x] 单次: 鼠标/键盘超过一分钟无任何响应(现在演示为10s)
- [ ] 单日24/0时
- [ ] 单月/周/年 1号/星期1/1月1号0时

## 提醒
### 连续工作N分钟/小时放送提醒
- [x] 默认半小时(30min), 10s一次提醒. 要终止提醒只能休息最少一分钟.
- [x] 强制锁屏 哈哈哈

### 周中连续N天超过N小时提醒
- [ ] 未实现
### 月中连续N天/M周超过C/Cc小时提醒
- [ ] 未实现

## 转换为`PySide6`
- 安装 pyside2 -> PySide6
- QAction
主要是:
```py
from PySide6.QtWidgets import QAction
```
换为:
```py
from PySide6.QtGui import QAction
```
- QSystemTrayIcon
```py
self.icon = self.MessageIcon()
```
需要从Enum中指定一个
```py
self.icon = self.MessageIcon(QSystemTrayIcon.MessageIcon.NoIcon)
```
- QtChats
```py
from PySide2.QtCharts import QtCharts
# PySide6 不能这么引入,不过我没用到就只是注释掉了
```
- 关闭进程
新版中`exec_`将不再支持, 需要使用`exec`:
```py
# sys.exit(app.exec_())
sys.exit(app.exec())
```