clear_logs:
	@rm  logs/*

docker_run_scraper:
	docker run --rm --network=arms-tracker_armstracker armstracker-scraper

docker_debug_scraper:
	docker run --rm -v /Users/freddy/code/Kafkaese/arms-tracker/data/databases:/data/database -e DB_PATH='data/databse/countries.sqlite' -it armstracker-scraper sh

docker_run_postgres:
	docker run --name armstracker-postgres -e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) -d -p 5432:5432 postgres