build:
	docker build --force-rm -t bankruptcy .
start:
	docker run --rm -v ${PWD}:/opt/bankruptcy-map --name bankruptcy -it -p 8888:8888 bankruptcy jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token= --notebook-dir='/opt/bankruptcy-map/notebooks'
bash:
	docker exec -it bankruptcy /bin/bash

