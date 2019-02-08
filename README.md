# products_service

Humanitec LogicModule backend service for products and inventory

## Development

Build the image:

```
docker-compose build
```

Run the web server:

```
docker-compose up
```

Open your browser with URL `http://localhost:8086`.
For the admin panel `http://localhost:8086/admin`
(user: `admin`, password: `admin`).

Run the tests only once:

```bash
docker-compose run --rm --entrypoint 'bash scripts/run-tests.sh' products_service
```

Run the tests and leave bash open inside the container, so it's possible to
re-run the tests faster again using `bash scripts/run-tests.sh [--keepdb]`:

```bash
docker-compose run --rm --entrypoint 'bash scripts/run-tests.sh --bash-on-finish' products_service
```

To run bash:

```bash
docker-compose run --rm --entrypoint 'bash' products_service
```
