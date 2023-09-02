## Introduction

Here is a simple CLI command which wraps [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/)

## Usage

```
docker run -v /path/templates/dir:/tmp/data --rm docker.pkg.github.com/kavw/cli/jinja:1.0.0 /tmp/data/example.jinja2 '{"username": "World"}'
```
