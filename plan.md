# 计划

## 进度

## 需求池
- [ ] 自定义存储`kv对` - 搜索框输入`A:B`格式数据按钮变换为保存, 可以保存`k v`形式数据, 以后在搜索框内输入`key`可以查找
- [ ] 无限粘贴板 - 监测系统粘贴板变化, 在搜索框键入`ztb`或者`cp`可以列出历史复制的所有内容, 并支持`ztb: 模糊查找关键字`语法查找内容
    ```py
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QClipboard

    app = QApplication()

    clipboard = app.clipboard()

    def on_clipboard_changed(mode):
        if mode == QClipboard.Clipboard:
            text = clipboard.text()
            print(f"Clipboard text: {text}")

    clipboard.dataChanged.connect(on_clipboard_changed)
    ```
- [ ] 做成pip包
- [ ] 其他实用功能

## 开发池
### 2023.03.29:
- [x] 优化搜索框样式
### 2021.04.03:
最基本功能已经实现啦.还有些丑,堪堪能用.
![v0.1界面展示](https://github.com/IanVzs/Halahayawa/blob/main/showme_v0.1.png "su mua~")
- [x] 界面
- [x] [yapf](#yapf)
- [x] [打包](#打包)
### 2021.04.07:
增加了记录按键此处展示
![v0.2界面展示](https://github.com/IanVzs/Halahayawa/blob/main/showme_v0.2.png "ha ha~")
### 2021.04.09:
增加了分阶段统计,不再是之前的汇总了.入库了也更容易监控操作
不过,还欠缺:
- [x] 在关闭窗口时记录阶段统计
- [x] 增加了工作转空闲缓冲时间可配置.
- [x] 相加一个主界面的轮询线程间隔可配置,现在是1s一次,好像也没啥必要.搞成5s也完全可以的.
### 2021.04.12:
- 增加了消息提醒
- 增加了主界面显示维度(现在有连续统计和总两个维度)
![v0.3界面展示](https://github.com/IanVzs/Halahayawa/blob/main/showme_v0.3.png "niu bi~")
### 2021.04.13:
- 开始打包啦,让朋友们用起来o(∩∩)o...哈哈
- 现在配置都是在运行启动参数里的,后面改成配置文件?
- [x] windows可执行程序包

### 2021.05.21
在macOS上修复了一个线程问题。。。蛮神奇的
不过使用`pyinstaller`打包貌似很麻烦, 以后有缘再打吧.

### 2023-01-16
- [x] 增加一个定时锁屏功能
- [x] 强制休息时间点到时, 强制锁屏

### 2023-03-17
- [x] 粘贴板操作工具
- [x] [升级到PySide6](#PySide6)
- [x] 转型成桌面脚本工具, 不在拘束在工作时长统计


## <a name="打包">打包</a>
- [x] `Linux`之后等功能完善后,以及打包问题解决后再上传
- [x] 目前图标展示还是和运行路径有关的,需要在`PySide6`里指明一下,另外打包时`PyInstaller`也不把`.ico`当作必要文件...也需要解决.

## <a name="yapf">yapf</a>
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

## <a name="PySide6">转换为`PySide6`涉及改动</a>
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
## 死需求池
- [ ] 锁屏前弹窗提示, 点击弹窗后可取消锁屏(离开工位自动锁屏功能 - 离开检测实在无法实现...)