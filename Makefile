clear_logs:
	@rm  logs/*

docker_run_scraper:
	docker run --rm -v /Users/freddy/code/Kafkaese/arms-tracker/data/databases:/data/database -e DB_PATH='data/databse/countries.sqlite' armstracker-scraper

docker_debug_scraper:
	docker run --rm -v /Users/freddy/code/Kafkaese/arms-tracker/data/databases:/data/database -e DB_PATH='data/databse/countries.sqlite' -it armstracker-scraper sh