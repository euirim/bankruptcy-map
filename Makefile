build:
	docker build -t bankruptcy .
start:
	docker run -v $(pwd)/notebooks:/opt/bankruptcy-map/notebooks -p 8888:8888 bankruptcy
