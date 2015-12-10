echo "127.0.0.1:11111 ---> Waiting for data..."
socat TCP4-LISTEN:11111,fork EXEC:./vul_heap,reuseaddr
