import json
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
from entityExtraction import findFinanceTerms
from searchcognitiveservice import findDescriptions

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


class AppService:
    
    tasks = [
        {
            'id': 1,
            'name': "task1",
            "description": "This is task 1"
        },
        {
            "id": 2,
            "name": "task2",
            "description": "This is task 2"
        },
        {
            "id": 3,
            "name": "task3",
            "description": "This is task 3"
        }
    ]

    def __init__(self):
        #results =  search_client.search(search_text="wifi", include_total_count=True, select='FinanceTermId,FinanceTerm,Description,Url')
        #print ('Total Documents Matching Query:', results.get_count())
        #for result in results:
        #    print("{}: {}: {}".format(result["FinanceTermId"], result["FinanceTerm"], result["Description"], result["Url"]))
        self.tasksJSON = json.dumps(self.tasks)

    def get_tasks(self):
        return self.tasksJSON

    def create_task(self,task):
        tasksData = json.loads(self.tasksJSON)
        tasksData.append(task)
        self.tasksJSON = json.dumps(tasksData)
        return self.tasksJSON

    def update_task(self, request_task):
        tasksData = json.loads(self.tasksJSON)
        for task in tasksData:
            if task["id"] == request_task['id']:
                task.update(request_task)
                return json.dumps(tasksData);
        return json.dumps({'message': 'task id not found'});

    def delete_task(self, request_task_id):
        tasksData = json.loads(self.tasksJSON)
        for task in tasksData:
            if task["id"] == request_task_id:
                tasksData.remove(task)
                return json.dumps(tasksData);
        return json.dumps({'message': 'task id not found'});

    def extract_terms(self, data):
        financeTerms = findFinanceTerms(data)
        print("financeTerms")
        print(financeTerms)
        financeTermToDescription = findDescriptions(financeTerms)
        financeTermsJson = json.dumps(financeTerms)
        return financeTermsJson


