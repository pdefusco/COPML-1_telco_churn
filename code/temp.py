
project_id = cml.get_project()['id']
params = {"projectId":project_id,"latestModelDeployment":True,"latestModelBuild":True}
model_id = cml.get_models(params)[0]['id']
latest_model = cml.get_model({"id": model_id, "latestModelDeployment": True, "latestModelBuild": True})


default_engine_details = cml.get_default_engine({})
default_engine_image_id = default_engine_details["id"]
build_model_params = {
  	"modelId": latest_model['latestModelBuild']['modelId'],
    "projectId": latest_model['latestModelBuild']['projectId'],
    "targetFilePath": "code/serve_eplained_model.py",
    "targetFunctionName": "explain",
    "engineImageId": default_engine_image_id,
    "kernel": "python3",
    "examples": latest_model['latestModelBuild']['examples'],
    "cpuMillicores": 1000,
    "memoryMb": 2048,
    "nvidiaGPUs": 0,
    "replicationPolicy": {"type": "fixed", "numReplicas": 1},
    "environment": {}}

  default_engine_details = cml.get_default_engine({})
  default_engine_image_id = default_engine_details["id"]
  build_model_params = {
      "modelId": model_id,
      "projectId": project_id,
      "targetFilePath": latest_model['latestModelBuild']['targetFilePath'],
      "targetFunctionName": latest_model['latestModelBuild']['targetFunctionName'],
      "engineImageId": default_engine_image_id,
      "kernel": "python3",
      "examples": latest_model['latestModelBuild']['examples'],
      "cpuMillicores": 1000,
      "memoryMb": 2048,
      "nvidiaGPUs": 0,
      "replicationPolicy": {"type": "fixed", "numReplicas": 1},
      "environment": {}}
  
  