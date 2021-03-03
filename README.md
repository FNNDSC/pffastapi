# FastAPI Customizable Router Package Example

## Usage

```bash
docker build -t local/notpfdcm .
```

### Run

```bash
docker run --rm -p 8000:8000 local/notpfdcm
```

### Development

```bash
docker run --rm -it -p 8000:8000 -v $PWD/notpfdcm:/app:ro  local/notpfdcm /start-reload.sh
```

See http://localhost:8000/docs

### Examples

Using [httpie](https://httpie.org/)

```bash
http :8000/api/v1/hello/ echoBack==lol
```

## Lessons Learned

A `setup.py` can be defined for the `pffastapi` package, then it can be published
to PyPI and used as a reusable set of routes.
Applications would import it as in `main.py`.

### Gotchas

`tiangolo/uvicorn-gunicorn-fastapi:python3.8` is used 
(instead of something more typical like `python:3.9.1-slim-buster`).
The relative import syntax from the tutorials on https://fastapi.tiangolo.com/
will not work.

https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/8748ba16cb9d4c8e4e5a99975438159ada14322c/docker-images/python3.8-slim.dockerfile#L18

Modules to be imported should always be defined in subdirectories with `__init__.py`.
