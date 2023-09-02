MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
PROJ_DIR := $(patsubst %/,%, $(dir $(MAKEFILE_PATH)))

DOCKER_IMAGE_NAME := jinja:1.0.0
DOCKER_TAG_LOCAL  := kavw/$(DOCKER_IMAGE_NAME)
DOCKER_TAG_PUBLIC := docker.pkg.github.com/kavw/cli/$(DOCKER_IMAGE_NAME)

DOCKER := docker
EXE_DOCKER_LOGIN := echo "$$GH_TOKEN" | $(DOCKER) login docker.pkg.github.com -u "$$GH_USER" --password-stdin
EXE_DOCKER_TAG := $(DOCKER) tag $(DOCKER_TAG_LOCAL) $(DOCKER_TAG_PUBLIC)
EXE_DOCKER_PUSH := $(DOCKER) push $(DOCKER_TAG_PUBLIC)

ifeq ($(OS),Windows_NT)
	PUSH_DEPS=win-push
else
	PUSH_DEPS=nix-push
endif

.PHONY: build
build:
	docker build --target app -t $(DOCKER_TAG_LOCAL) -f $(PROJ_DIR)/Dockerfile .
	docker run -v $(PROJ_DIR)/tests/data:/tmp/data --rm $(DOCKER_TAG_LOCAL) /tmp/data/example.jinja2 '{"username": "World"}'

.PHONY: win-push
win-push:
	cmd /C $(PROJ_DIR)/.Makefile.env.bat
	$(EXE_DOCKER_TAG)
	$(EXE_DOCKER_PUSH)

.PHONY: nix-push
nix-push:
	@set -eu; . $(PROJ_DIR)/.Makefile.env; \
	$(EXE_DOCKER_LOGIN); \
	$(EXE_DOCKER_TAG); \
	$(EXE_DOCKER_PUSH);

.PHONY: push
push: $(PUSH_DEPS)
	$(DOCKER) run -v $(PROJ_DIR)/tests/data:/tmp/data --rm $(DOCKER_TAG_PUBLIC) /tmp/data/example.jinja2 '{"username": "World"}'
	@echo "Done"

.PHONY: docker
docker:
	docker build --target basic -t kavw/jinja:basic -f $(PROJ_DIR)/Dockerfile .
	docker run -it --rm kavw/jinja:basic bash
