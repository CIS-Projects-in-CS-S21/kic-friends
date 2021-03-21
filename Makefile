.DEFAULT_GOAL := run_tests

push:
	docker build -t gcr.io/keeping-it-casual/kic-friends:dev .
	docker push gcr.io/keeping-it-casual/kic-friends:dev