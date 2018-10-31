[![Build Status](https://travis-ci.com/kai25/docker-command-tool.svg?branch=master)](https://travis-ci.com/kai25/docker-command-tool)

# docker-command-tool
It is simple wrapper around docker.
It makes possible to create some cli in your project (building static, generate protobuf, etc.).

Example of using:
```sh
$ pip install bagga
$ bagga some_come command
```

Example of dct.yaml:

```yaml
containers:
  static-container: |
    FROM alpine:3.7
    RUN apk add --update nodejs nodejs-npm

  app-container: |
    FROM jfloff/alpine-python
    WORKDIR workdir
    COPY server .
    RUN pip install -r requirements

commands:
  build-js:
    container: static-container
    volumes:
      ~/project:/opt/project
    cmd: |
      echo 'building js'
      echo 'ok'

  build-css:
      container: static-container
      cmd: |
        echo 'building css'
        echo 'ok'

  run:
    container: app-container
    ports:
      5000:5000
    cmd: |
      FLASK_APP=run.py python -m flask run
```

Run:
```sh
$ python dct.py build-css
```

## bagga params
Command | Description
------- | -----------
`-d [--docker-commands] '{commands}'` | Add custom docker commands for `docker run`
`-c [--config] '{config_path}'` | Use custom config file instead of `dct.yaml`
