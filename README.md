# COPML Example 1 - Telco Churn
This repoistory is used as the first example in the [Continuous Operations for Production Machine Learning (COPML) document](https://linktothis.com) that provides a framework for maintaning machine learning projects in production. The repository contains all the artifacts needed to reproduce the end-to-end example on running [Cloudera Machine Learning (CML)](https://docs.cloudera.com/machine-learning/cloud/index.html) or [Cloudera Data Science Workbench (CDSW)](https://docs.cloudera.com/cdsw/1.9.1/index.html) instance. The data used in this project is integrated into the wider [Cloudera Data Platform (CDP)](https://www.cloudera.com/products/cloudera-data-platform.html). This project uses the [Applied ML Prototype (AMP)](https://docs.cloudera.com/machine-learning/cloud/applied-ml-prototypes/topics/ml-amps-overview.html) format and will automatically deploy the models and jobs needed to run the complete project when using CML.

![table_view](images/table_view.png)

The primary goal of this repo is to build a logistic regression classification model to predict the probability that a group of customers will churn from a fictitious telecommunications company. 

This project follows the most common basic steps for building and maintaining machine learning projects in production:
* Step 1: Clarify Business Requirements
* Step 2: Assess Available Data
* Step 3: Develop the Data Science Plan
* Step 4: Model Deployment
* Step 5: Model Operations

The project also provides all the necessary building blocks to create a complete, end-to-end machine learning project that meets all the requirements required as part of the COPML process:

#### Business Requirements
* Availability
* Effectiveness
* Automation
* Risk Management

#### Regulatory Requirements
* Auditability
* Reproducability
* Explainabilty

By following the notebooks in the `notebooks` directory, and the scripts and documentation in the `code` directory, you will understand how to perform similar classification tasks using CML on your data. You will also be able to build and maintain a machine learning project in production that can continue to be useful and deliver value to the you business. 

This project works best if deploy as an Applied ML Prototype, 

## Project Structure

The project is organized with the following folder structure:

```
.
├── app/                    # Assets needed to support the front end application
├── code/                   # Scripts and code needed to create project artifacts
├── images/                 # A collection of images referenced in project docs
├── models/                 # Directory to hold trained models
├── notebooks/              # Notebooks for data and model eploration
├── data/                   # The raw data file used within the project
├── .project-metadata.yaml  # The AMP specification file
├── cdsw-build.sh           # Shell script used to build environment for experiments and models
├── lineage.yml             # Model lineage file used for model governance
├── README.md
└── requirements.txt
```

This project focuses on working within CML, using all it has to offer, while glossing over the details that are simply standard data science. We trust that you are familiar with typical data science concepts and do not need additional explanations for some of the code.

If you have deployed this project as an Applied ML Prototype (AMP), you will not need to run any of the setup steps outlined [in this document](code/README.md) as the Application, Model and Jobs are already installed for you. However, you should  review the documentation and their corresponding files to see how this project fits with the COPML framework.