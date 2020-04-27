#!/bin/bash
echo ""
echo "_-_-_-_-_-_-_-_-_-_-_-_-_-_-"
echo "Esta es tu ip publica"
host myip.opendns.com resolver1.opendns.com | grep "myip.opendns.com has" | awk '{print $4}'
echo "______________________"
