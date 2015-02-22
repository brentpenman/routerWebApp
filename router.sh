#!/bin/bash
source=$(echo "obase=16;ibase=10; $1" | bc)
dest=$(echo "obase=16;ibase=10; $2" | bc)
sum=$(($1 + $2 + 1))
hexsum=$(echo "obase=16;ibase=10; $sum" | bc)

exec 4<>/dev/tcp/192.168.2.214/5001;
echo -ne '\x12\x00\x'$hexsum'\x00\x00\x08' >&4;
echo -ne '\x00\x'$source'\x00\x'$dest'\x00\x00\x00\x01' >&4 ;



