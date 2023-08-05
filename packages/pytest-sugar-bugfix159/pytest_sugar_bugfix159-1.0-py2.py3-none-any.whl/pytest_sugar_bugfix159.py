def pytest_configure():
	"https://github.com/Frozenball/pytest-sugar/159"
	import pytest_sugar
	pytest_sugar.SugarTerminalReporter.pytest_runtest_logfinish = \
		lambda self: None
