

from datetime import datetime
import json
import logging
from kubernetes import client, config
from kubernetes.client import api_client
# Configs can be set in Configuration class directly or using helper utility
from rules import *

def main():
    
    aConfiguration = config.load_kube_config()
    aApiClient = client.ApiClient(aConfiguration)
    v1 = client.CoreV1Api(aApiClient)
    print("Listing all pods in the cluster:")

    RUNNING_STATUS = "Running" 

    rules = [image_prefix_check, team_label_present_check, recent_start_time_check]

    pods = v1.list_pod_for_all_namespaces(watch=False)
    for item in pods.items:
        status = str(item.status.phase)
        if status == RUNNING_STATUS:
            pod_name = item.metadata.name
            start_time = item.status.start_time       
            pod_result = PodResult(pod_name)        
            for rule in rules:
                try:
                    rule_result = rule.check(item)             
                    pod_result.add_rule_result(rule_result)
                except Exception as e:
                    logging.error(e)
            output = pod_result.to_json()
            print(output)
        
if __name__ == '__main__':
    main()
        



