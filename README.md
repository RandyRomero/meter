# meter

A simple task assignment.
An app that creates a random int and publishes it to rabbitmq once
in a while.

### Requirements

Requires running rabbitmq. Host, port, login, password can be configured
via environment variables.

### Installation
```
git clone git@github.com:RandyRomero/meter.git

cd meter

poetry shell

poetry install
```

### Formatting and CI

`make format`

`make check`

### Tests

To be written