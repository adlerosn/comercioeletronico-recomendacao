default: test
	@echo "SUCCESS"

test: database.db
	@bash testaMenu1-1.sh
	@bash testaMenu1-2.sh
	@bash testaMenu2-1.sh
	@bash testaMenu3-1.sh

database.db:
	@bash montaDb.sh
