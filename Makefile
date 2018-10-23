.PHONY : build tests server

server : build
	docker run --name tornado_tcp_server -p 8888:8888 -p 8889:8889 -d tornado_tcp_server

tests : build
	docker run --name tornado_tcp_server_tests --rm tornado_tcp_server tests

build :
	docker build -t tornado_tcp_server .