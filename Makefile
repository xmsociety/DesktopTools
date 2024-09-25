.PHONY: help

# Put it first so that "make" without argument is like "make help".
help: # 获取命令行示例
	@grep ":" Makefile | grep -v "Makefile"

check:
	python .\scripts\check.py

format:
	isort DesktopTools
	black DesktopTools
	flake8 --ignore W503,E203,E501,E731,F403,F401 DesktopTools --exclude ui_searchbar.py,searchbar_ui.py,venv/
doc:
	pip install sphinx myst_parser

poetry: # 有新的库包引入,推代码需要先验证的
	pip install -U pip setuptools
	pip install poetry
	python -m poetry lock

run: # 运行
	python test.py
build: # pip安装
	pip install .[ui]
	@echo "instal sucess: DesktopTools"
ui: # 编译.ui 到 .py
	cd DesktopTools/feather_hotkey && pyside6-uic searchbar.ui -o ui_searchbar.py

edit_ui:
	find DesktopTools/ -name *.ui
	pyside6-designer DesktopTools/feather_hotkey/searchbar.ui