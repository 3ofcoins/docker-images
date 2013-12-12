docker-sentry
=============

Sentry packaged as a Docker image. Only PostgreSQL database is
supported.

Environment variables
---------------------

 - `PGHOST` (default: Docker host)
 - `PGPORT` (default: 5432)
 - `PGDATABASE` (default: sentry)
 - `PGUSER` (default: sentry)
 - `PGPASSWORD` (default: sentry)
 - `SENTRY_URL_PREFIX`
 - `SENTRY_WEB_WORKERS` (default: 3) - number of gunicorn workers to start
 - `SENTRY_WEB_REMOTE_USER_AUTH` - if set, it's name of the HTTP
   request dictionary that will be trusted to contain username
   (e.g. `HTTP_REMOTE_USER`).
 - `CELERY_ALWAYS_EAGER` - if set, then Celery won't be used even if
   Redis connection is configured
 - `REDIS_DATABASE` (default: 0) - Redis database number to use

Linked Containers
-----------------

If a linked container named `postgresql` is provided, its IP & port
will be used as `PGHOST` & `PGPORT` (remaining postgres variables will
be normally interpreted).

If a linked container named `memcache` exists, it will be used as
cache. Alternatively, you can provide environment variable
`MEMCACHE_PORT="tcp://HOST:PORT"`.

If a linked container named `redis` exists, it will be used for Celery
task queue and for buffers. Alternatively, you can provide environment
variable `REDIS_PORT="tcp://HOST:PORT"`.

Running
-------

The `sentry` command is configured as the entry point, so simply
running `docker run mpasternacki/sentry server` will start the Web
server.
