import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient 
from azure.search.documents import SearchClient
from azure.search.documents.indexes.models import (
    ComplexField,
    CorsOptions,
    SearchIndex,
    ScoringProfile,
    SearchFieldDataType,
    SimpleField,
    SearchableField
)

service_name = "financetermdetails"
admin_key = "x6u7a1gn9oajlKtFIA6GNg7gCgdmx13V0Ndjkmnay2AzSeBtkkZO"

index_name = "finance-term"

# Create an SDK client
endpoint = "https://financetermdetails.search.windows.net/".format(service_name)
admin_client = SearchIndexClient(endpoint=endpoint,
                    index_name=index_name,
                    credential=AzureKeyCredential(admin_key))

search_client = SearchClient(endpoint=endpoint,
                       index_name=index_name,
                       credential=AzureKeyCredential(admin_key))

def main():
    documents = [
        {
        "@search.action": "upload",
        "FinanceTermId":"1",
        "FinanceTerm": "test finance name",
        "Description": "Testing the description and the likes",
        "Url": "https://test-me.com"
        } 
    ]
    print(documents)

def upload_files(document_to_upload):
    try:
        result = search_client.upload_documents(documents=document_to_upload)
        print("Upload of new document succeeded: {}".format(result[0].succeeded))
    except Exception as ex:
        print (ex.message)


if __name__ == "__main__":
    main()