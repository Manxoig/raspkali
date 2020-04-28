#!/bin/bash
echo ""
 echo ".- -- .- / ... ..- .- .-.-."
echo "Esta es tu ip publica"
host myip.opendns.com resolver1.opendns.com | grep "myip.opendns.com has" | awk '{print $4}'
 echo ".- -- .- / ... ..- .- .-.-."
 echo ""
