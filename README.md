[![Build Status](https://travis-ci.com/kai25/docker-command-tool.svg?branch=master)](https://travis-ci.com/kai25/docker-command-tool)

# docker-command-tool
It is simple wrapper around docker.
It makes possible to create some cli in your project (building static, generating protobuf, etc.).

Example of using:
```sh
$ pip install bagga
$ bagga some_command
```

Example of dct.yaml:

```yaml
containers:
  static-container: |
    FROM node:8
    RUN echo 'some actions'
    
  app-container: |
    FROM python:3.6.6-stretch
    WORKDIR workdir
    COPY server .
    RUN pip install -r requirements

commands:
  build-js:
    container: static-container
    volumes:
      $(pwd):/opt/project
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
    volumes:
      /your-machine/verywow:/docker/verywow
    ports:
      5000:5000
    envs:
      MY_SUPREME_ENV='my_env'
    cmd: |
      FLASK_APP=run.py python -m flask run
```

Run:
```sh
$ bagga build-css
```

## bagga params
Command | Description
------- | -----------
`-d [--docker-commands] '{commands}'` | Add custom docker commands for `docker run`
`-c [--config] '{config_path}'` | Use custom config file instead of `dct.yaml`
