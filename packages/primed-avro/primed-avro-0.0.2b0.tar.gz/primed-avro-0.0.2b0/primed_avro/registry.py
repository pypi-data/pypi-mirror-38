import requests
from schema import SchemaMeta


class ConfluentSchemaRegistryClient:
    def __init__(self, url):
        self.url = url

    def get_schema(self, subject, version="latest"):
        r = requests.get(
            "{url}/subjects/{subject}/versions/{version}".format(
                url=self.url, subject=subject, version=version
            ),
            headers={"Content-Type": "application/vnd.schemaregistry.v1+json"},
        )

        if r.status_code == 200:
            js = r.json()

            if "error_code" in js:
                raise Exception(
                    "failed to retrieve schema, error_code: {error_code}, msg: {msg}".format(
                        error_code=js["error_code"], msg=js["msg"]
                    )
                )

            return SchemaMeta(**js)
        else:
            raise Exception(
                "failed to retrieve schema due to connection problems, status code: {status_code}".format(
                    status_code=r.status_code
                )
            )
