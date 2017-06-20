echo "2\n3\n\n0\n" | python3 ../cli.py | grep -e "^| *[0-9]* *|" | cut -d'|' -f2 | sed -e 's/^ *//' | sed -e 's/ *$//'
