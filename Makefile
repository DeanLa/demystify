.PHONY: class another
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

###
class: ## strip solution notebooks to hide exercises
	python runner.py strip

strip: class

backup: ## Backup all solution notebooks
	python runner.py backup

rmnb: ## Remove class notebooks
	python runner.py rmnb