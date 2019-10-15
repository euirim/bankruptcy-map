build:
	docker build --rm -t bankruptcy .
start:
	docker run --rm -v ${PWD}:/opt/bankruptcy-map -it -p 8888:8888 bankruptcy jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token= --notebook-dir='/opt/bankruptcy-map/notebooks'
