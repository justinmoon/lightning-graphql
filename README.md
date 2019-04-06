# Lightning-GraphQL

The goal of this project is to create a GraphQL endpoint that can create invoice, query, and pay Lightning invoices. It is implemented as a c-lightning plugin.

# Development Setup

### Installations
- Install bitcoind
- Install c-lightning
- Install lnet
- Have lnet make some connections: `./launch.sh 10 2`
- Install lnet-random
- Have lnet-random make some invoices: `node activity.js`
- Copy `example_config.py` to `config.py` and fill out the variables
- Create a virtual environment and install requirements:
```
python3 -m venv venv
source venv/bin/activate
pip instal -r requirements.txt
```

### Running Examples

##### Test Queries on Command Line

```
(venv) $ python lightning_graphql.py
```
