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

index_name = "finance-term-full"

# Create an SDK client
endpoint = "https://financetermdetails.search.windows.net/".format(service_name)
admin_client = SearchIndexClient(endpoint=endpoint,
                    index_name=index_name,
                    credential=AzureKeyCredential(admin_key))

search_client = SearchClient(endpoint=endpoint,
                       index_name=index_name,
                       credential=AzureKeyCredential(admin_key))

def main():
    #search=FinanceTerm:Economic~ AND Integrations~&queryType=full
    #whatever phrases or words we get 
    #if they are multiple add an AND between each and ~ for the fuzzy search 
    results =  search_client.search(search_text="FinanceTerm:Economic~ AND Integratio~", query_type="full", include_total_count=True, select='FinanceTermId,FinanceTerm,Description,Url')
    print ('Total Documents Matching Query:', results.get_count())
    for result in results:
        print("{}: {}: {}".format(result["FinanceTermId"], result["FinanceTerm"], result["Description"], result["Url"]))


def upload_files(document_to_upload):
    try:
        result = search_client.upload_documents(documents=document_to_upload)
        print("Upload of new document succeeded: {}".format(result[0].succeeded))
    except Exception as ex:
        print (ex.message)

def findDescriptions(financeTerms):
    details = []
    print("trying to find the descriptions")
    for term in financeTerms:
        termSplit = term.split(" ")
        searchString = ""
        for word in termSplit:
            searchString = searchString + word
            searchString = searchString + "~" + " "
        print("searchString")
        print(searchString)

        results = search_client.search(search_text=searchString, query_type="full", top=1, include_total_count=True, select='FinanceTermId,FinanceTerm,Description,Url')
        #print ('Total Documents Matching Query:', result.get_count())
        print(results)
        print ('Total Documents Matching Query:', results.get_count())
        #print("{}: {}: {} : {}".format(result["FinanceTermId"], result["FinanceTerm"], result["Description"], result["Url"], result["@search.score"]))
        for result in results:
            print("{}: {}: {} : {}".format(result["FinanceTermId"], result["FinanceTerm"], result["Description"], result["Url"], result["@search.score"]))
            print(result)
    return details


if __name__ == "__main__":
    main()