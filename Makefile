fmt:
	cd src && autoflake --in-place --remove-all-unused-imports --recursive .
	cd src && isort .
	cd src && black .