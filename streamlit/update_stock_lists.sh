#!/usr/bin/env bash

ntxt="nasdaq.txt"
ttxt="tsx.txt"

http 'https://api.nasdaq.com/api/screener/stocks?tableonly=false&limit=9999&offset=0' | jq -r '.data.table.rows[] | .symbol' > $ntxt & 
http 'https://stockanalysis.com/api/screener/a/f?m=marketCap&s=desc&c=no,s,marketCap&f=exchange-is-TSX,subtype-isnot-etf!cef&dd=true&i=symbols' | jq -r '.data.data[] | .s' | sed 's/tsx\///' > $ttxt &


wait


echo "Wrote $(wc -l < $ntxt) lines to $ntxt"
echo "Wrote $(wc -l < $ttxt) lines to $ttxt"



