echo "127.0.0.1:11112 ---> Waiting for data..."
socat TCP4-LISTEN:11112,fork EXEC:./vul_uaf,reuseaddr
