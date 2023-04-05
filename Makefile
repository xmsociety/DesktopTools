.PHONY: help

# Put it first so that "make" without argument is like "make help".
help: # 获取命令行示例
	@grep ":" Makefile | grep -v "Makefile"

code_check:
	isort --check --diff DesktopTools
	black --check --diff DesktopTools
	flake8 --ignore W503,E203,E501,E731,F403,F401 . --exclude DesktopTools/feather_hotkey/searchbar.ui,venv/,DesktopTools/feather_hotkey/ui_searchbar.py

format:
	isort DesktopTools
	black DesktopTools
	flake8 --ignore W503,E203,E501,E731,F403,F401 DesktopTools --exclude DesktopTools/feather_hotkey/searchbar.ui,venv/,DesktopTools/feather_hotkey/ui_searchbar.py

run: # 运行
	python test.py
build: # pip安装
	pip install .[ui]
	@echo "instal sucess: DesktopTools"
ui: # 编译.ui 到 .py
	cd DesktopTools/feather_hotkey && pyside6-uic searchbar.ui -o ui_searchbar.py