echo "127.0.0.1:22222 ---> Waiting for data..."
socat TCP4-LISTEN:22222,fork EXEC:./vul_fstr,reuseaddr
