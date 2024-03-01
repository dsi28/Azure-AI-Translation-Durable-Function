# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging

from azure.durable_functions import DurableOrchestrationContext, Orchestrator



def orchestrator_function(context: DurableOrchestrationContext):
    
    source_sas = context.get_input()
    # step 1:
        #  places source blob in new source container
        #  create destination container in blob storage
        #  return sas blob sas urls for both newly created containers
    destination_sas = yield context.call_activity('SetupActivity', source_sas)

    logging.warning(f'des {destination_sas}')
    # step 2:
        #  document translation activity function
        #  translates document in source container 
        #  and places translated document in destination container
    translated_doc_location = yield context.call_activity('TranslationActivity', [source_sas,destination_sas] )

    # step 3:
        #  get translated document
        #  see if its possible to return translated document from this activity function to the orchestrator to the starter to client
    # result3 = yield context.call_activity('Translate1', "London")

    # step 4:
        #  clean up
        #  delete source container
        #  rename destination conatiner to done-currentContainerName
    # result3 = yield context.call_activity('Translate1', "London")

    return translated_doc_location
    # return [result1, result2, result3]

main = Orchestrator.create(orchestrator_function)