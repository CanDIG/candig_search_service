# CanDIG cross-service search application

More or less a PoC currently. Offers a graphql interface with the help
of the tartiflette framework.

## Running in Development

Development dependencies are described in `requirements.txt` and can be
installed using the following command:

```bash
pip install -r requirements.txt
```

To start the application:

```bash
python -m search_service
```

The visual query builder is available at /graphiql, otherwise the main
endpoint is at /graphql
