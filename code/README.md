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
#