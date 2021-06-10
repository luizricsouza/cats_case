# Cats Case

Foobar is a Python library for dealing with word pluralization.

## Instalação

Para subir o ambiente, executar o docker-compose na pasta da aplicação.

```bash
docker-compose up
```

## Uso da API

```bash
curl --location --request GET 'localhost:5000/cats_breeds'
curl --location --request GET 'localhost:5000/cats_breeds?temperament=active'
curl --location --request GET 'localhost:5000/cats_breeds?origin=egypt'
curl --location --request GET 'localhost:5000/cats_breeds?origin=egypt&temperament=active'
curl --location --request GET 'http://localhost:5000/breed_info?breed_name=aegean'
```
## Log API


