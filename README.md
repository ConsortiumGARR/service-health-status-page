# Neanias Services Status Page

## Deploy on K8s cluster

1. Create a docker-registry secret in order to allow the cluster to pull the image


    $ kubectl create secret docker-registry neanias-registry --docker-username=<registry_username> --docker-email=<registry_email> --docker-password=<registry_pull_registry_token>
    --docker-server=<private_registry_url>

2. Create a secret with the InfluxDB credentials:

    $ kubectl apply -f status-page-secret.yaml

3. Create a k8s service for the deployment:

    $ kubectl apply -f status-page-service.yaml

4. Create a k8s deployment for the application ( nginx + flask web app):

    $ kubectl apply -f status-page-deployment.yaml

## Development

### Requirements

- pip3
- virtualenv

### Setup environment

Create a virtual environment:

    $ virtualenv create venv

Create a .env file with InfluxDB credentials:

    cp .env.example .env

Fill the .env file with the credentials

### Run the flask application

Enable the virtualenv

    $ source venv/bin/activate

You can run the webapp in debug mode running the provided bash script:

    $ bash ./run_dev_env.sh


## Test
TBD

