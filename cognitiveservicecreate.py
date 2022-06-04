#!pip install azure-search-documents --pre
#!pip show azure-search-documents

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

service_name = ""
admin_key = ""

index_name = "finance-term"

# Create an SDK client
endpoint = "https://financetermdetails.search.windows.net/".format(service_name)
admin_client = SearchIndexClient(endpoint=endpoint,
                    index_name=index_name,
                    credential=AzureKeyCredential(admin_key))

search_client = SearchClient(endpoint=endpoint,
                       index_name=index_name,
                       credential=AzureKeyCredential(admin_key))

try:
    result = admin_client.delete_index(index_name)
    print ('Index', index_name, 'Deleted')
except Exception as ex:
    print (ex)


# Specify the index schema
name = index_name
fields = [
        SimpleField(name="FinanceTermId", type=SearchFieldDataType.String, key=True),
        SearchableField(name="FinanceTerm", type=SearchFieldDataType.String),
        SearchableField(name="Description", type=SearchFieldDataType.String, analyzer_name="en.lucene"),
        SearchableField(name="Url", type=SearchFieldDataType.String)
    ]
cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
scoring_profiles = []
suggester = [{'name': 'sg', 'source_fields': ['Tags', 'Address/City', 'Address/Country']}]


index = SearchIndex(
    name=name,
    fields=fields,
    scoring_profiles=scoring_profiles,
    #suggesters = suggester,
    cors_options=cors_options)

try:
    result = admin_client.create_index(index)
    print ('Index', result.name, 'created')
except Exception as ex:
    print (ex)