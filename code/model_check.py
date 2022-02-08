# # Check Model
# This file should be run in a job that will periodically check the current model's accuracy and trigger the 
# model retrain job if its below the required thresh hold. 

import cdsw, time, os
import pandas as pd
from sklearn.metrics import classification_report
from cmlbootstrap import CMLBootstrap



# replace this with these values relevant values from the project
cml = CMLBootstrap()
for job in cml.get_jobs():
  if job['name'] == "Train Model":
    job_id = job['name']


import cmlapi
try:
    client = cmlapi.default_client()
except ValueError:
    print("Could not create a client. If this code is not being run in a CML session, please include the keyword arguments \"url\" and \"cml_api_key\".")

project_id = os.environ["CDSW_PROJECT_ID"]
    
# gather model details
model = (
    client.list_models(project_id=project_id, async_req=True)
    .get()
    .to_dict()
)

model_id = model["models"][0]["id"]
model_crn = model["models"][0]["crn"]

builds = (
    client.list_model_builds(
        project_id=project_id, model_id=model_id, async_req=True
    )
    .get()
    .to_dict()
)
build_info = builds["model_builds"][-1]  # most recent build

build_id = build_info["id"]


# gather latest deployment details
deployments = (
    client.list_model_deployments(
        project_id=project_id,
        model_id=model_id,
        build_id=build_id,
        async_req=True
    )
    .get()
    .to_dict()
)
deployment_info = deployments["model_deployments"][-1]  

model_deployment_crn = deployment_info["crn"]

# Read in the model metrics dict.
model_metrics = cdsw.read_metrics(model_crn=model_crn,model_deployment_crn=model_deployment_crn)

# This is a handy way to unravel the dict into a big pandas dataframe.
metrics_df = pd.io.json.json_normalize(model_metrics["metrics"])

latest_aggregate_metric = metrics_df.dropna(subset=["metrics.accuracy"]).sort_values('startTimeStampMs')[-1:]["metrics.accuracy"]


if latest_aggregate_metric.to_list()[0] < 0.6:
  print("model is below threshold, retraining")
  cml.start_job(job_id,{})
  
else:
  print("model does not need to be retrained")
