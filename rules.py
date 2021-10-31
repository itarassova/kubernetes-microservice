PREFIX = "bitnami"
LABEL = "team"
RUNTIME = 7

import json
from datetime import datetime

def time_conversion(start_time):
    fmt = '%Y-%m-%d %H:%M:%S'
    tstamp1 = datetime.strptime(str(start_time).split("+")[0], fmt)
    current_time = datetime.now()
    tstamp2 = datetime.strptime(str(current_time).split(".")[0], fmt)
    running_time = int(round(abs((tstamp2 - tstamp1).total_seconds()) /86400))
    return running_time 
    
def image_prefix_check(item):
    for container in item.spec.containers:
            image = str(container.image)
            if not image.startswith(PREFIX):
                return False
    return True

def team_label_present_check(item):
    if str(item.metadata.labels.keys) == LABEL:
        if not str(item.metadata.labels.value).is_empty(): 
            return True
    return False

def recent_start_time_check(item):
    start_time = item.status.start_time
    running_time = time_conversion(start_time)
    if running_time > RUNTIME:
        return False
    return True

class PodResult:
    def __init__(self, pod):
        self.pod = pod
        self.pod_results = []

    def add_rule_result(self, rule_result):
        self.pod_results.append(rule_result)

    def to_json(self):
        return json.dumps(self, default = lambda o: o.__dict__, sort_keys = True, separators=(',', ':'))


# {rule_name: "", result: ""}
class RuleResult:
    def __init__(self, rule_name, result):
        self.name = rule_name
        self.result = result



class Rule:
    def __init__(self, rule_name :str, description : str, check_function):
        self.name = rule_name
        self.description = description
        self.check_function = check_function

    def check(self, pod) -> RuleResult:
        return RuleResult(self.name, self.check_function(pod))

image_prefix_check = Rule("image_prefix", "ensure the pod only uses images prefixed with `bitnami/`", image_prefix_check)
team_label_present_check = Rule("team_label_present", "ensure the pod contains a label `team` with some value", team_label_present_check)
recent_start_time_check = Rule("recent_start_time", "ensure the pod has not been running for more than 7 days according to it's `startTime`", recent_start_time_check)      
        
