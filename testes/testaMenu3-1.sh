#!/bin/sh
source colors.sh
echo -e "${COLOR_LIGHT_RED}\c"
EXPECTED="| 1               |  80.00% |     ???% |
| 2               |  80.00% |   20.00% |
| 3               |  60.00% |    0.00% |"
FOUND=$(sh runTest3-1.sh)
echo -e "${COLOR_NC}\c"
if [ "$EXPECTED" == "$FOUND" ]
then
  echo -e "${COLOR_LIGHT_GREEN}PASS${COLOR_NC}"
else
  echo -e "${COLOR_RED}FAIL${COLOR_NC}"
  echo "Expected $EXPECTED and found $FOUND"
  error
fi
