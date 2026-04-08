.PHONY: build test test-cov test-html clean

IMAGE_NAME = easyinsta

build:
	docker build -t $(IMAGE_NAME) -f ci/Dockerfile .

test: build
	docker run --rm $(IMAGE_NAME) pytest

test-cov: build
	docker run --rm $(IMAGE_NAME) pytest --cov=easyinsta --cov-report=term-missing

test-html: build
	docker run --rm -v $(PWD)/htmlcov:/app/htmlcov $(IMAGE_NAME) pytest --cov=easyinsta --cov-report=html

clean:
	rm -rf htmlcov .coverage .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
