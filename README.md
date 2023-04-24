# Currency Exchange Backend

This is the backend solution for the Backend Oriented Task Dynatrance 2023 in Gdansk, realized by **Szymon Nagel** as part of a recruitment process. It is designed to provide exchange rate data using [NBP API](http://api.nbp.pl/)

## Requirements

- Python 3.10
- pip

## Installation

1. Clone the repository:

```
git clone https://github.com/My5z0n/currency-exchange-backend.git
```

2. Install the required packages:

```
cd currency-exchange-backend
pip install -r ./app/requirements.txt
```

3. Start the server:

```
python3 ./app/main.py
```

## Endpoints

The following endpoints are available:

- `[GET] /exchange-rate/a/{currency_code}/{date}` - Get the exchange rate for a specific currency code and date. 

- `[GET] /exchange-rate/a/max_min_average/{currency_code}/{num_quotations}` - Get the maximum and minimum of exchange rates for a given currency code over the specified number of quotations.  

- `[GET] /exchange-rate/c/major-difference/{currency_code}/{num_quotations}` - Get the largest difference in exchange rates for a given currency code over the specified number of quotations. 

## Docker

A Dockerfile and docker-compose.yml file are included for containerization.

To build the Docker image:

```
docker build -f "app/dockerfile" -t currency-exchange-backend:latest "app"
```

To run the Docker container:

```
docker run -p 80:80 -e APP_ENV=dev currencyexchangebackend:latest
```

Alternatively it is possible to use docker-compose in prod/dev versions:

```
docker compose -f "docker-compose.yaml" up -d --build
```

## Testing

This project uses [pytest](https://docs.pytest.org/en/latest/) for testing. To run the tests, make sure you have `pytest` installed:

```
pip install pytest
```

Then, from the root directory of the project, run:

```
pytest ./app/tests
```

For more information on how to use `pytest`, refer to the [official documentation](https://docs.pytest.org/en/latest/).

## GitHub Actions

Two GitHub Actions are included:

- `on-pr`: Runs all Pytest tests build docker image on a pull request to the thamin branch
- `build-and-push`: Provides basic CI (Continuous Integration) it builds the Docker container on a push to the main branch and pushes docker image to remote [Docker Hub](https://hub.docker.com/r/szmnnagel/currency-exchange-backend).

## License

This project is licensed under the GPLv3. See the [LICENSE](LICENSE) file for details.
