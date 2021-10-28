

from datetime import datetime
import json
from kubernetes import client, config
from kubernetes.client import api_client
# Configs can be set in Configuration class directly or using helper utility
from rules import *

def main():

    #aToken = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ik1xNEpwYmEwc3VYVXZtdnlGTlBMZmh1VUxEWUtmZFdVVGRxdkdEYVBkbTQifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tOWRicTciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6Ijk4YjM5YTVlLTc4NDktNGRjOS04Y2YzLWNkZmUwYTQzNTNkMCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.i-dBJmNs6eYWGE-yIpO78tEi6XI1aJAUEaYt5oLDsX8asvRpGFRvifGupBJFNYu2EdSD9s9GZsNPrYQ2HKDuGeTS_agNyfo07QcYZ4dRYEdofPNmS2YTul94VNHi5rgMK3d1K4m5zXBaZYQ5QpkxdJE49JVv-2KzYn_V_700RKVx4AjJ8CxqF_vflY2x2E463YzM3VGrQBIlL7BMgPc1ptZTtZqEUIGO8l0RoqQqqM1XacT24MiNxcitjoY5hhplW6tjQneQb-lO2XDei4qQFPqN1J8_4tktd1s-llDGh3LM0PNqlAZX2sBI6FS_8PvXRdiqVdTlJMocu1ynaxe6iQ"
    #aConfiguration = client.Configuration()
    #aConfiguration.host = "https://127.0.0.1:54514"
    #aConfiguration.verify_ssl = False
    #aConfiguration.api_key = {"authorisation": "Bearer" + aToken}
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
                rule_result = rule.check(item)             
                pod_result.add_rule_result(rule_result)
            output = pod_result.to_json()
            print(output)
        
if __name__ == '__main__':
    main()
        



