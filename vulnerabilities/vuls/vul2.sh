echo "127.0.0.1:12345 ---> Waiting for data..."
socat TCP4-LISTEN:12345,fork EXEC:./vul2
