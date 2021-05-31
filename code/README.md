## Part 1: Data Ingest
A data scientist should never be blocked in getting data into their environment,
so CML is able to ingest data from many sources.
Whether you have data in .csv files, modern formats like parquet or feather,
in cloud storage or a SQL database, CML will let you work with it in a data
scientist-friendly environment.

Access local data on your computer
#
Accessing data stored on your computer is a matter of [uploading a file to the CML filesystem and
referencing from there](https://docs.cloudera.com/machine-learning/cloud/import-data/topics/ml-accessing-local-data-from-your-computer.html).
#
> Go to the project's **Overview** page. Under the **Files** section, click **Upload**, select the relevant data files to be uploaded and a destination folder.
#
If, for example, you upload a file called, `mydata.csv` to a folder called `data`, the
following example code would work.

```
import pandas as pd
#
df = pd.read_csv('data/mydata.csv')
#
Or:
df = pd.read_csv('/home/cdsw/data/mydata.csv')
```

Access data in S3
#
Accessing [data in Amazon S3](https://docs.cloudera.com/machine-learning/cloud/import-data/topics/ml-accessing-data-in-amazon-s3-buckets.html)
follows a familiar procedure of fetching and storing in the CML filesystem.
> Add your Amazon Web Services access keys to your project's
> [environment variables](https://docs.cloudera.com/machine-learning/cloud/import-data/topics/ml-environment-variables.html)
> as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
#
To get the the access keys that are used for your in the CDP DataLake, you can follow
[this Cloudera Community Tutorial](https://community.cloudera.com/t5/Community-Articles/How-to-get-AWS-access-keys-via-IDBroker-in-CDP/ta-p/295485)

#
The following sample code would fetch a file called `myfile.csv` from the S3 bucket, `data_bucket`, and store it in the CML home folder.
```
Create the Boto S3 connection object.
from boto.s3.connection import S3Connection
aws_connection = S3Connection()
#
Download the dataset to file 'myfile.csv'.
bucket = aws_connection.get_bucket('data_bucket')
key = bucket.get_key('myfile.csv')
key.get_contents_to_filename('/home/cdsw/myfile.csv')
```


Access data from Cloud Storage or the Hive metastore
#
Accessing data from [the Hive metastore](https://docs.cloudera.com/machine-learning/cloud/import-data/topics/ml-accessing-data-from-apache-hive.html)
that comes with CML only takes a few more steps.
But first we need to fetch the data from Cloud Storage and save it as a Hive table.
#
> Specify `STORAGE` as an
> [environment variable](https://docs.cloudera.com/machine-learning/cloud/import-data/topics/ml-environment-variables.html)
> in your project settings containing the Cloud Storage location used by the DataLake to store
> Hive data. On AWS it will `s3a://[something]`, on Azure it will be `abfs://[something]` and on
> on prem CDSW cluster, it will be `hdfs://[something]`
#
This was done for you when you ran `0_bootstrap.py`, so the following code is set up to run as is.
It begins with imports and creating a `SparkSession`.

## Model Training

This script is used to train an Explained model and also how to use the
Jobs to run model training and the Experiments feature of CML to facilitate model
tuning.

If you haven't yet, run through the initialization steps in the README file and Part 1.
In Part 1, the data is imported into the `default.telco_churn` table in Hive.
All data accesses fetch from Hive.
#
To simply train the model once, run this file in a workbench session.
#
There are 2 other ways of running the model training process
#
***Scheduled Jobs***
#
The **[Jobs](https://docs.cloudera.com/machine-learning/cloud/jobs-pipelines/topics/ml-creating-a-job.html)**
feature allows for adhoc, recurring and depend jobs to run specific scripts. To run this model
training process as a job, create a new job by going to the Project window and clicking _Jobs >
New Job_ and entering the following settings:
* **Name** : Train Mdoel
* **Script** : 4_train_models.py
* **Arguments** : _Leave blank_
* **Kernel** : Python 3
* **Schedule** : Manual
* **Engine Profile** : 1 vCPU / 2 GiB
The rest can be left as is. Once the job has been created, click **Run** to start a manual
run for that job.

***Experiments***
#
Training a model for use in production requires testing many combinations of model parameters
and picking the best one based on one or more metrics.
In order to do this in a *principled*, *reproducible* way, an Experiment executes model training code with **versioning** of the **project code**, **input parameters**, and **output artifacts**.
This is a very useful feature for testing a large number of hyperparameters in parallel on elastic cloud resources.

**[Experiments](https://docs.cloudera.com/machine-learning/cloud/experiments/topics/ml-running-an-experiment.html)**.
run immediately and are used for testing different parameters in a model training process.
In this instance it would be use for hyperparameter optimisation. To run an experiment, from the
Project window click Experiments > Run Experiment with the following settings.
* **Script** : 4_train_models.py
* **Arguments** : 5 lbfgs 100 _(these the cv, solver and max_iter parameters to be passed to
LogisticRegressionCV() function)
* **Kernel** : Python 3
* **Engine Profile** : 1 vCPU / 2 GiB

Click **Start Run** and the expriment will be sheduled to build and run. Once the Run is
completed you can view the outputs that are tracked with the experiment using the
`cdsw.track_metrics` function. It's worth reading through the code to get a sense of what
all is going on.

More Details on Running Experiments
Requirements
Experiments have a few requirements:
- model training code in a `.py` script, not a notebook
- `requirements.txt` file listing package dependencies
- a `cdsw-build.sh` script containing code to install all dependencies
#
These three components are provided for the churn model as `4_train_models.py`, `requirements.txt`,
and `cdsw-build.sh`, respectively.
You can see that `cdsw-build.sh` simply installs packages from `requirements.txt`.
The code in `4_train_models.py` is largely identical to the code in the last notebook.
with a few differences.
#
The first difference from the last notebook is at the "Experiments options" section.
When you set up a new Experiment, you can enter
[**command line arguments**](https://docs.python.org/3/library/sys.html#sys.argv)
in standard Python fashion.
This will be where you enter the combination of model hyperparameters that you wish to test.
#
The other difference is at the end of the script.
Here, the `cdsw` package (available by default) provides
[two methods](https://docs.cloudera.com/machine-learning/cloud/experiments/topics/ml-tracking-metrics.html)
to let the user evaluate results.
#
**`cdsw.track_metric`** stores a single value which can be viewed in the Experiments UI.
Here we store two metrics and the filepath to the saved model.
#
**`cdsw.track_file`** stores a file for later inspection.
Here we store the saved model, but we could also have saved a report csv, plot, or any other
output file.
#

## Part 5 Model Serving
#
This notebook explains how to create and deploy Models in CML which function as a 
REST API to serve predictions. This feature makes it very easy for a data scientist 
to make trained models available and usable to other developers and data scientists 
in your organization.
#
In the last part of the series, you learned: 
- the requirements for running an Experiment
- how to set up a new Experiment
- how to monitor the results of an Experiment
- limitations of the feature
#
In this part, you will learn:
- the requirements for creating and deploying a Model
- how to deploy a Model
- how to test and use a Model
- limitations of the feature
#
If you haven't yet, run through the initialization steps in the README file and Part 1. 
In Part 1, the data is imported into the `default.telco_churn` table in Hive. 
All data accesses fetch from Hive.
#
### Requirements
Models have the same requirements as Experiments:
- model code in a `.py` script, not a notebook
- a `requirements.txt` file listing package dependencies
- a `cdsw-build.sh` script containing code to install all dependencies
#
> In addition, Models *must* be designed with one main function that takes a dictionary as its sole argument
> and returns a single dictionary.
> CML handles the JSON serialization and deserialization.

In this file, there is minimal code since calculating predictions is much simpler 
than training a machine learning model.
Once again, we use the `ExplainedModel` helper class in `churnexplainer.py`.
When a Model API is called, CML will translate the input and returned JSON blobs to and from python dictionaries.
Thus, the script simply loads the model we saved at the end of the last notebook,
passes the input dictionary into the model, and returns the results as a dictionary with the following format:
   
   {
       'data': dict(data),
       'probability': probability,
       'explanation': explanation
   }
#
The Model API will return this dictionary serialized as JSON.

### Model Operations

This model is deployed using the model operations feature of CML which consists of 
[Model Metrics](https://docs.cloudera.com/machine-learning/cloud/model-metrics/topics/ml-enabling-model-metrics.html)
and [Model Governance](https://docs.cloudera.com/machine-learning/cloud/model-governance/topics/ml-enabling-model-governance.html)

The first requirement to make the model use the model metrics feature by adding the 
`@cdsw.model_metrics` [Python Decorator](https://wiki.python.org/moin/PythonDecorators)
before the fuction. 
#
Then you can use the *`cdsw.track_metric`* function to add additional
data to the underlying database for each call made to the model. 
**Note:** `cdsw.track_metric` has different functionality depening on if its being 
used in an *Experiment* or a *Model*.

More detail is available
using the `help(cdsw.track_mertic)` function
#```
help(cdsw.track_metric)
Help on function track_metric in module cdsw:
#
track_metric(key, value)
   Description
   -----------
   
   Tracks a metric for an experiment or model deployment
       Example:
           model deployment usage:
               >>>@cdsw.model_metrics
               >>>predict_func(args):
               >>>   cdsw.track_metric("input_args", args)
               >>>   return {"result": "prediction"}
   
           experiment usage:
               >>>cdsw.track_metric("input_args", args)
   
   Parameters
   ----------
   key: string
       The metric key to track
   value: string, boolean, numeric
       The metric value to track
#```
#
#
### Creating and deploying a Model
To create a Model using our `5_model_serve_explainer.py` script, use the following settings:
* **Name**: Explainer
* **Description**: Explain customer churn prediction
* **File**: `5_model_serve_explainer.py`
* **Function**: explain
* **Input**: 
```
{
	"StreamingTV": "No",
	"MonthlyCharges": 70.35,
	"PhoneService": "No",
	"PaperlessBilling": "No",
	"Partner": "No",
	"OnlineBackup": "No",
	"gender": "Female",
	"Contract": "Month-to-month",
	"TotalCharges": 1397.475,
	"StreamingMovies": "No",
  "DeviceProtection": "No",
  "PaymentMethod": "Bank transfer (automatic)",
  "tenure": 29,
  "Dependents": "No",
  "OnlineSecurity": "No",
  "MultipleLines": "No",
  "InternetService": "DSL",
  "SeniorCitizen": "No",
  "TechSupport": "No"
}
```
#* **Kernel**: Python 3
#* **Engine Profile**: 1 vCPU / 2 GiB Memory
#
The rest can be left as is.
#
After accepting the dialog, CML will *build* a new Docker image using `cdsw-build.sh`,
then *assign an endpoint* for sending requests to the new Model.

## Testing the Model
> To verify it's returning the right results in the format you expect, you can 
> test any Model from it's *Overview* page.
#
If you entered an *Example Input* before, it will be the default input here, 
though you can enter your own.

## Using the Model
#
> The *Overview* page also provides sample `curl` or Python commands for calling your Model API.
> You can adapt these samples for other code that will call this API.
#
This is also where you can find the full endpoint to share with other developers 
and data scientists.
#
**Note:** for security, you can specify 
[Model API Keys](https://docs.cloudera.com/machine-learning/cloud/models/topics/ml-model-api-key-for-models.html) 
to add authentication.

## Limitations
#
Models do have a few limitations that are important to know:
- re-deploying or re-building Models results in Model downtime (usually brief)
- re-starting CML does not automatically restart active Models
- Model logs and statistics are only preserved so long as the individual replica is active
#
A current list of known limitations are 
[documented here](https://docs.cloudera.com/machine-learning/cloud/models/topics/ml-models-known-issues-and-limitations.html).


## Part 6: Application

This script explains how to create and deploy Applications in CML.
This feature allows data scientists to **get ML solutions in front of stakeholders quickly**,
including business users who need results fast.
This may be good for sharing a **highly customized dashboard**, a **monitoring tool**, or a **product mockup**.

CML is agnostic regarding frameworks.
[Flask](https://flask.palletsprojects.com/en/1.1.x/),
[Dash](https://plotly.com/dash/),
or even [Tornado](https://www.tornadoweb.org/en/stable/) apps will all work.
R users will find it easy to deploy Shiny apps.

If you haven't yet, run through the initialization steps in the README file. Do that
now

This file is provides a sample Flask app script, ready for deployment,
which displays churn predictions and explanations using the Model API deployed in
Part 5

Deploying the Application
#
> Once you have written an app that is working as desired, including in a test Session,
> it can be deployed using the *New Application* dialog in the *Applications* tab in CML.

After accepting the dialog, CML will deploy the application then *assign a URL* to
the Application using the subdomain you chose.
#
*Note:* This does not requirement the `cdsw-build.sh* file as it doen now follows a
seperate build process to deploy an application.
#

To create an Application using our sample Flask app, perform the following.
This is a special step for this particular app:
#
In the deployed Model from step 5, go to *Model* > *Settings* in CML and make a note (i.e. copy) the
"**Access Key**". eg - `mqc8ypo...pmj056y`
#
While you're there, **disable** the additional Model authentication feature by unticking **Enable Authentication**.
#
**Note**: Disabling authentication is only necessary for this Application to work.
Ordinarily, you may want to keep Authentication in place.
#
Next, from the Project level, click on *Open Workbench* (note you don't actually have to Launch a
Session) in order to edit a file. Select the `flask/single_view.html` file and paste the Access
Key in at line 19.
#
`        const accessKey = "mp3ebluylxh4yn5h9xurh1r0430y76ca";`
#
Save the file (if it has not auto saved already) and go back to the Project.
#
Finally, go to the *Applications* section of the Project and select *New Application* with the following:
* **Name**: Churn Analysis App
* **Subdomain**: churn-app _(note: this needs to be unique, so if you've done this before,
pick a more random subdomain name)_
* **Script**: 6_application.py
* **Kernel**: Python 3
* **Engine Profile**: 1 vCPU / 2 GiB Memory
#
Accept the inputs, and in a few minutes the Application will be ready to use.

Using the Application

>  A few minutes after deploying, the *Applications* page will show the app as Running.
You can then click on its name to access it.
CML Applications are accessible by any user with read-only (or higher) access to the project.
#

This deploys a basic flask application for serving the HTML and some specific data
use for project Application.

At this point, you will be able to open the Churn Analysis App.
The initial view is a table of randomly selected customers from the dataset.
This provides a snapshot of the customer base as a whole.
The colors in the *Probability* column correspond to the prediction, with red customers being deemed more likely to churn.
The colors of the features show which are most important for each prediction.
Deeper red indicates incresed importance for predicting that a customer **will churn**
while deeper blue indicates incresed importance for predicting that a customer **will not**.

## Part 7 - Model Operations - Visualising Model Metrics

This is a continuation of the previous process started in the 
`7a_ml_ops_simulations.py` script.
Here we will load in the metrics saved to the model database in the previous step 
into a Pandas dataframe, and display different features as graphs. 

```python
help(cdsw.read_metrics)
Help on function read_metrics in module cdsw:

read_metrics(model_deployment_crn=None, start_timestamp_ms=None, end_timestamp_ms=None, model_crn=None, model_build_crn=None)
   Description
   -----------
   
   Read metrics data for given Crn with start and end time stamp
   
   Parameters
   ----------
   model_deployment_crn: string
       model deployment Crn
   model_crn: string
       model Crn
   model_build_crn: string
       model build Crn
   start_timestamp_ms: int, optional
       metrics data start timestamp in milliseconds , if not passed
       default value 0 is used to fetch data
   end_timestamp_ms: int, optional
       metrics data end timestamp in milliseconds , if not passed
       current timestamp is used to fetch data
   
   Returns
   -------
   object
       metrics data
```