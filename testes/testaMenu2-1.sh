#!/bin/sh
source colors.sh
echo -e "${COLOR_RED}\c"
EXPECTED="1"
FOUND=$(sh runTest2-1.sh)
echo -e "${COLOR_NC}\c"
if [ "$EXPECTED" == "$FOUND" ]
then
  echo -e "${COLOR_LIGHT_GREEN}PASS${COLOR_NC}"
else
  echo -e "${COLOR_RED}FAIL${COLOR_NC}"
  echo "Expected $EXPECTED and found $FOUND"
  error
fi
