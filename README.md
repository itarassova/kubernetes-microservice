# kubernetes-microservice

# pod-checker

Pod-checker is a python script to verify pod adherence to specific rules:

```yaml
rules:
- name: image_prefix
  description: "ensure the pod only uses images prefixed with `bitnami/`"
  output: boolean
- name: team_label_present
  description: "ensure the pod contains a label `team` with some value"
  output: boolean
- name: recent_start_time
  description: "ensure the pod has not been running for more than 7 days according to it's `startTime`"
  output: boolean
```

Output is produced on the STDOUT as follows:

```json
{"pod": "mytest", "rule_evaluation": [{"name": "image_prefix", "valid": true}, {"name": "team_label_present", "valid": true}, {"name": "recent_start_time", "valid": false}]}
{"pod": "another", "rule_evaluation": [{"name": "image_prefix", "valid": false}, {"name": "team_label_present", "valid": true}, {"name": "recent_start_time", "valid": false}]}


## Installation

use 

`docker build .` to create a runnable docker image

and

`docker run $IMAGE_NAME` to execute the container produced in the previous step


## License
[MIT](https://choosealicense.com/licenses/mit/)
