# CanDIG cross-service search application

More or less a PoC currently. Offers a graphql interface with the help
of the tartiflette framework.

## Configuration

At the root of this project there is a sample dotenv file (.env-sample). These can be
exported as environment variables or used as is. Simply copy the sample file and
provide the missing values.

```bash
cp .env-sample .env
```

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

## How it works

You may look at the GraphQL schema in search_service/sdl/Query.graphql
As it stands this schema is built manually, by collecting the schema
produced by the metadata service and adding any further objects (to
represent other data source / microservices).

Each of these objects then correspond to 

## GraphQL querying

Here is an example of what's possible to query:

```
{
  # We want every patient, filtered by gender
  patients(gender: "male") {
    # In GraphQL we have to specify every field we want in the response
    # (i.e. there are no wildcard - by design)
    name,
    patientId,
    dateOfBirth,
    gender,
    # For every patient, with want a list of corresponding
    # objects (this is also provided by the metadata service)
    complications {
      name,
      description,
      date
    },
    consents {
      consentDate,
      consentVersion
    },
    chemotherapies {
      startDate,
      stopDate,
      type
    },
    samples {
      sampleId,
      name,
      quantity,
      # Except this - this nested object is resolved by querying a
      # remote service, htsget (by way of the sampleId)
      sampleUrls {
        url
      }
    }
  }
}
```

Behind the scenes, this translate to one call to the metadata service
for the patients and its nested objects + for each sample found, a
call is made to get the sampleUrls. Performance-wise this is suboptimal
of course, further caching and optimization awaits.
