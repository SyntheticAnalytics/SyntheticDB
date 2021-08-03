build:
	poetry build

publish:
	poetry publish

bump:
	poetry version patch

release: bump build publish

test:
	pytest