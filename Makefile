clear_logs:
	@rm  logs/*

docker_run_scraper:
	docker run --rm --network=arms-tracker_armstracker --env-file '.env' armstracker-scraper

docker_rebuild_run_scraper:
	docker build -f docker/dockerfiles/Dockerfile_scraping -t armstracker-scraper .
	docker run --rm --network=arms-tracker_armstracker --env-file '.env' armstracker-scraper
	
docker_debug_scraper:
	docker run --rm --network=arms-tracker_armstracker --env-file '.env' -it armstracker-scraper sh

docker_run_postgres:
	docker run --name armstracker-postgres -e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) -d -p 5432:5432 postgres