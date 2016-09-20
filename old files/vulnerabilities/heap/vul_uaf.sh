echo "127.0.0.1:34568 ---> Waiting for data..."
socat TCP4-LISTEN:34568,fork EXEC:./vul_uaf
