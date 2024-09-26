# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build

# Function to check if sphinx-build exists
check_sphinx:
	@command -v $(SPHINXBUILD) >/dev/null 2>&1 || { \
		echo "Error: $(SPHINXBUILD) not found."; \
		echo "You can check your Python installation with: whereis python"; \
		exit 1; \
	}

# Put it first so that "make" without argument is like "make help".
help: check_sphinx
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile check_sphinx

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile check_sphinx
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
