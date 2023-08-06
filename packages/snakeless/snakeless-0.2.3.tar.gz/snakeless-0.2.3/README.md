# Snakeless [![image](https://img.shields.io/pypi/v/snakeless.svg)](https://python.org/pypi/snakeless) [![image](https://img.shields.io/pypi/l/snakeless.svg)](https://python.org/pypi/snakeless) [![image](https://img.shields.io/pypi/pyversions/snakeless.svg)](https://python.org/pypi/snakeless)

> Write true serverless apps with joy

## Description

**Snakeless** is a tool that tries to simplify deployment of serverless apps on
different platforms. 

It is easily extensible by plugins. You can write a plugin for additional functionality 
or a wrapper for new service provider!

Plugins for providers:
- [Google Cloud](https://github.com/Tasyp/snakeless-provider-gcloud)
- Feel free to write your own!

## Features
-   Supports multiple serverless providers.
-   Loads `.env` Automatically. 
-   Configuration is done in one simple `.yaml` file
-   Wide range of available aspects to configure.
-   Deploy all functions at once or by one - you choose!
-   *WIP*: Possible to invoke functions locally 

## Usage

We use [poetry](https://github.com/sdispater/poetry) for dependency management and publishing.

### Installation
```
$ pip install snakeless 
```

### Development

```
$ poetry instal 
```

### Testing
```
WIP
```

## Documentation
WIP

## Contributions

Feel free to send some [pull request](https://github.com/Tasyp/snakeless/pulls) or [issue](https://github.com/Tasyp/snakeless/issues).

## License
MIT license

© 2018 [German Ivanov](https://github.com/Tasyp)
