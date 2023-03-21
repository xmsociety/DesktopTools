.PHONY: help

# Put it first so that "make" without argument is like "make help".
help: # 获取命令行示例
	@grep ":" Makefile | grep -v "Makefile"

code_check:
	isort --check --diff .
	black --check --diff .
	flake8 --ignore W503,E203,E501,E731,F403,F401 . --exclude feather_hotkey/searchbar.ui,venv/

format:
	isort .
	black .
	flake8 --ignore W503,E203,E501,E731,F403,F401 . --exclude feather_hotkey/searchbar.ui,venv/

run: # 运行
	python main.py
ui: # 编译.ui 到 .py
	cd feather_hotkey && pyside6-uic searchbar.ui -o ui_searchbar.py