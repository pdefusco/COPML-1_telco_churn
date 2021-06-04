
# Churn Prediction Prototype
This project is a Cloudera Machine Learning 
([CML](https://www.cloudera.com/products/machine-learning.html)) **Applied Machine Learning 
Project Prototype**. It has all the code and data needed to deploy an end-to-end machine 
learning project in a running CML instance.

## Project Overview
This project builds the telco churn with model interpretability project discussed in more 
detail [this blog post](https://blog.cloudera.com/visual-model-interpretability-for-telco-churn-in-cloudera-data-science-workbench/). 
The initial idea and code comes from the FFL Interpretability report which is now freely 
available and you can read the full report [here](https://ff06-2020.fastforwardlabs.com/)

![table_view](images/table_view.png)

The goal is to build a classifier model using Logistic Regression to predict the churn 
probability for a group of customers from a telecoms company. On top that, the model 
can then be interpreted using [LIME](https://github.com/marcotcr/lime). Both the Logistic 
Regression and LIME models are then deployed using CML's real-time model deployment 
capability and finally a basic flask based web application is deployed that will let 
you interact with the real-time model to see which factors in the data have the most 
influence on the churn probability.

By following the notebooks in this project, you will understand how to perform similar 
classification tasks on CML as well as how to use the platform's major features to your 
advantage. These features include **streamlined model experimentation**, 
**point-and-click model deployment**, and **ML app hosting**.

We will focus our attention on working within CML, using all it has to offer, while
glossing over the details that are simply standard data science.
We trust that you are familiar with typical data science workflows
and do not need detailed explanations of the code.
Notes that are *specific to CML* will be emphasized in **block quotes**.

### Initialize the Project
There are a couple of steps needed at the start to configure the Project and Workspace 
settings so each step will run sucessfully. You **must** run the project bootstrap 
before running other steps. If you just want to launch the model interpretability 
application without going through each step manually, then you can also deploy the 
complete project. 

***Project bootstrap***

Open the file `0_bootstrap.py` in a normal workbench python3 session. You only need a 
1 vCPU / 2 GiB instance. Once the session is loaded, click **Run > Run All Lines**. 
This will file will create an Environment Variable for the project called **STORAGE**, 
which is the root of default file storage location for the Hive Metastore in the 
DataLake (e.g. `s3a://my-default-bucket`). It will also upload the data used in the 
project to `$STORAGE/datalake/data/churn/`. The original file comes as part of this 
git repo in the `raw` folder.
  
***Deploy the Complete Project***

If you just wish build the project artifacts without going through each step manually, 
run the `8_build_projet.py` file in a python3 session. Again a 1 vCPU / 2 GiB instance 
will be suffient. This script will: 
* run the bootstrap
* then create the Hive Table and import the data
* deploy the model
* update the application files to use this new model
* deploy the application
* run the model drift simulation
Once the script has completed you will see the new model and application are now available 
in the project.

## Project Build
If you want go through each of the steps manually to build and understand how the project 
works, follow the steps below. There is a lot more detail and explanation/comments in each 
of the files/notebooks so its worth looking into those. Follow the steps below and you 
will end up with a running application.

### 0 Bootstrap
Just to reiterate that you have run the bootstrap for this project before anything else. 
So make sure you run step 0 first. 

Open the file `0_bootstrap.py` in a normal workbench python3 session. You only need a 
1 CPU / 2 GB instance. Then **Run > Run All Lines**

### 1 Ingest Data
This script will read in the data csv from the file uploaded to the object store (s3/adls) setup 
during the bootstrap and create a managed table in Hive. This is all done using Spark.

Open `1_data_ingest.py` in a Workbench session: python3, 1 CPU, 2 GB. Run the file.

### 2 Explore Data
This is a Jupyter Notebook that does some basic data exploration and visualistaion. It 
is to show how this would be part of the data science workflow.

![data](images/data.png)

Open a Jupyter Notebook session (rather than a work bench): python3, 1 CPU, 2 GB and 
open the `2_data_exploration.ipynb` file. 

At the top of the page click **Cells > Run All**.

### 3 Model Building
This is also a Jupyter Notebook to show the process of selecting and building the model 
to predict churn. It also shows more details on how the LIME model is created and a bit 
more on what LIME is actually doing.

Open a Jupyter Notebook session (rather than a work bench): python3, 1 CPU, 2 GB and 
open the `	3_model_building.ipynb` file. 

At the top of the page click **Cells > Run All**.

### 4 Model Training
A model pre-trained is saved with the repo has been and placed in the `models` directory. 
If you want to retrain the model, open the `4_train_models.py` file in a workbench  session: 
python3 1 vCPU, 2 GiB and run the file. The newly model will be saved in the models directory 
named `telco_linear`. 

There are 2 other ways of running the model training process

***1. Jobs***

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

***2. Experiments***

The other option is running an **[Experiment](https://docs.cloudera.com/machine-learning/cloud/experiments/topics/ml-running-an-experiment.html)**. Experiments run immediately and are used for testing different parameters in a model training process. In this instance it would be use for hyperparameter optimisation. To run an experiment, from the Project window click Experiments > Run Experiment with the following settings.
* **Script** : 4_train_models.py
* **Arguments** : 5 lbfgs 100 _(these the cv, solver and max_iter parameters to be passed to 
LogisticRegressionCV() function)
* **Kernel** : Python 3
* **Engine Profile** : 1 vCPU / 2 GiB

Click **Start Run** and the expriment will be sheduled to build and run. Once the Run is 
completed you can view the outputs that are tracked with the experiment using the 
`cdsw.track_metrics` function. It's worth reading through the code to get a sense of what 
all is going on.


### 5 Serve Model
The **[Models](https://docs.cloudera.com/machine-learning/cloud/models/topics/ml-creating-and-deploying-a-model.html)** 
is used top deploy a machine learning model into production for real-time prediction. To 
deploy the model trailed in the previous step, from  to the Project page, click **Models > New
Model** and create a new model with the following details:

* **Name**: Explainer
* **Description**: Explain customer churn prediction
* **File**: 5_model_serve_explainer.py
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
* **Kernel**: Python 3
* **Engine Profile**: 1vCPU / 2 GiB Memory

Leave the rest unchanged. Click **Deploy Model** and the model will go through the build 
process and deploy a REST endpoint. Once the model is deployed, you can test it is working 
from the model Model Overview page.

_**Note: This is important**_

Once the model is deployed, you must disable the additional model authentication feature. In the model settings page, untick **Enable Authentication**.

![disable_auth](images/disable_auth.png)

### 6 Deploy Application
The next step is to deploy the Flask application. The **[Applications](https://docs.cloudera.com/machine-learning/cloud/applications/topics/ml-applications.html)** feature is still quite new for CML. For this project it is used to deploy a web based application that interacts with the underlying model created in the previous step.

_**Note: This next step is important**_

_In the deployed model from step 5, go to **Model > Settings** and make a note (i.e. copy) the 
"Access Key". It will look something like this (ie. mukd9sit7tacnfq2phhn3whc4unq1f38)_

_From the Project level click on "Open Workbench" (note you don't actually have to Launch a 
session) in order to edit a file. Select the flask/single_view.html file and paste the Access 
Key in at line 19._

`        const accessKey = "mp3ebluylxh4yn5h9xurh1r0430y76ca";`

_Save the file (if it has not auto saved already) and go back to the Project._

From the Go to the **Applications** section and select "New Application" with the following:
* **Name**: Churn Analysis App
* **Subdomain**: churn-app _(note: this needs to be unique, so if you've done this before, 
pick a more random subdomain name)_
* **Script**: 6_application.py
* **Kernel**: Python 3
* **Engine Profile**: 1vCPU / 2 GiB Memory


After the Application deploys, click on the blue-arrow next to the name. The initial view is a 
table of randomly selected from the dataset. This shows a global view of which features are 
most important for the predictor model. The reds show incresed importance for preditcting a 
cusomter that will churn and the blues for for customers that will not.

![table_view](images/table_view.png)

Clicking on any single row will show a "local" interpreted model for that particular data point 
instance. Here you can see how adjusting any one of the features will change the instance's 
churn prediction.


![single_view_1](images/single_view_1.png)

Changing the InternetService to DSL lowers the probablity of churn. *Note: this does not mean 
that changing the Internet Service to DSL cause the probability to go down, this is just what 
the model would predict for a customer with those data points*


![single_view_2](images/single_view_2.png)

### 7 Model Operations
The final step is the model operations which consists of [Model Metrics](https://docs.cloudera.com/machine-learning/cloud/model-metrics/topics/ml-enabling-model-metrics.html)
and [Model Governance](https://docs.cloudera.com/machine-learning/cloud/model-governance/topics/ml-enabling-model-governance.html)

**Model Governance** is setup in the `0_bootstrap.py` script, which writes out the lineage.yml file at
the start of the project. For the **Model Metrics** open a workbench session (1 vCPU / 2 GiB) and open the
`7a_ml_ops_simulation.py` file. You need to set the `model_id` number from the model created in step 5 on line
113. The model number is on the model's main page.

![model_id](images/model_id.png)

`model_id = "95"`

From there, run the file. This goes through a process of simulating an model that drifts over 
over 1000 calls to the model. The file contains comments with details of how this is done.

In the next step you can interact and display the model metrics. Open a workbench 
session (1 vCPU / 2 GiB) and open and run the `7b_ml_ops_visual.py` file. Again you 
need to set the `model_id` number from the model created in step 5 on line 53. 
The model number is on the model's main page.

![model_accuracy](images/model_accuracy.png)



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