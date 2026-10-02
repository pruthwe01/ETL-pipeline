from ckanapi import RemoteCKAN

rc = RemoteCKAN("https://data.gov.au/data/")
result = rc.action.datastore_search(
    resource_id="591cb009-1167-4008-b7e8-f5fc9dbbb511",
    limit=5,
)
print(result["fields"])
print(result["records"])