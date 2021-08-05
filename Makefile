build:
	poetry build

publish:
	poetry publish

bump:
	poetry version patch

release: bump build publish

format:
	black syntheticdb/ tests/

test:
	pytest