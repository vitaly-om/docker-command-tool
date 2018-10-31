[![Build Status](https://travis-ci.com/kai25/docker-command-tool.svg?branch=master)](https://travis-ci.com/kai25/docker-command-tool)

# docker-command-tool

You need installed pyyaml to run script.

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
    cmd: |
      FLASK_APP=run.py python -m flask run
```

Run:
```sh
$ python dct.py build-css
```

If you need to pass params for container running(volumes, port exposing, etc.):
```sh
$ python dct.py run dp '-p 5000:5000'
```

## bagga params
Command | Description
------- | -----------
`-d [--docker-commands] '{commands}'` | Add custom docker commands for `docker run`
`-c [--config] '{commands}'` | Use custom config file instead of `dct.yaml`
