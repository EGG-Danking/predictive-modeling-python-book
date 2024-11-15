



build:
	quarto render docs/
	open docs/_build/index.html

preview:
	quarto preview docs/

render:
	quarto render docs/

open:
	open docs/_build/index.html

open-pdf:
	open docs/_build/Predictive-Modeling-in-Python.pdf



render-fresh:
	rm -rf docs/_build
	rm -rf docs/.quarto
	quarto render docs/
