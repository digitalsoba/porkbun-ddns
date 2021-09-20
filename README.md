# porkbun-ddns
This Python script updates DNS entries of a Porkbun subdomain.
This is mainly used to dynamically update DNS entries in case my ISP reassigns a new address.

## Using the python script
### Requirements
- Python 3.9+
- Porkbun API and secret key
- Preferably use a virtual environment

Install `requirements.txt`packages with `pip install -r requirements.txt`

Export your Porkbun keys as environment variables
```
export PORKBUN_API_KEY=123456
export PORKBUN_SECRET_KEY=123456
```

Run the python script with the following --domain and --subdomain flags
```
python main.py -d example.com -s test
```

## Run using docker
```
docker run \
-e PORKBUN_API_KEY=$PORKBUN_API_KEY \
-e PORKBUN_SECRET_KEY=$PORKBUN_SECRET_KEY \
-e DOMAIN=example.com \
-e SUBDOMAIN=test \
digitalsoba/porkbun-ddns:latest
```