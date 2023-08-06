# Pacifica Smart Proxy Service
[![Build Status](https://travis-ci.org/pacifica/pacifica-proxy.svg?branch=master)](https://travis-ci.org/pacifica/pacifica-proxy)
[![Build status](https://ci.appveyor.com/api/projects/status/b57r43intftb1fu9?svg=true)](https://ci.appveyor.com/project/dmlb2000/pacifica-proxy)
[![Code Climate](https://codeclimate.com/github/pacifica/pacifica-proxy/badges/gpa.svg)](https://codeclimate.com/github/pacifica/pacifica-proxy)
[![Test Coverage](https://codeclimate.com/github/pacifica/pacifica-proxy/badges/coverage.svg)](https://codeclimate.com/github/pacifica/pacifica-proxy/coverage)
[![Issue Count](https://codeclimate.com/github/pacifica/pacifica-proxy/badges/issue_count.svg)](https://codeclimate.com/github/pacifica/pacifica-proxy)
[![Docker Stars](https://img.shields.io/docker/stars/pacifica/proxy.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/proxy/general)
[![Docker Pulls](https://img.shields.io/docker/pulls/pacifica/proxy.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/proxy/general)
[![Docker Automated build](https://img.shields.io/docker/automated/pacifica/proxy.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/proxy/builds)

This service provides external access with some basic logic to redirect or
obfuscate access to other Pacifica services that are intended to be internal
only.

## Files Access

The [archive interface service](https://github.com/pacifica/pacifica-archiveinterface)
is intended to be used by internal services to access files off the archive by
file ID only. This can be easily iterated over by external users and should not
be exposed externally. This service accepts a hashsum provided by the user and
looks up a file ID based on that hashsum. The service then redirects the request
without knowledge of the user to the archive interface to pull the file.

### File Access API

Example curl command
```
curl http://localhost:8180/files/sha1/f90a581a5099079a8f1f582dd3643b6e060cc551
```

If the file exists the file is given as an octet-stream to the user. The
disposition header is also set with the filename defined in the metadata for
that file.

If the file does not exist a `404 Not Found` return code is given.

### Configuration

If you are running this service behind nginx or apache this service can take
advantage of proxy server configurations to remove a layer of redirection
through this service that isn't needed.

The [nginx configuration documentation](https://www.nginx.com/resources/wiki/start/topics/examples/x-accel/)
describes how to set this up and example nginx.conf files are provided in our
testing framework (`travis/nginx.conf.in`).
