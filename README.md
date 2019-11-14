# Excel Killer - Learning-App [![Build Status](https://travis-ci.com/anshu0612/Excel-Killer-E-Learning-App.svg?branch=master)](https://travis-ci.com/anshu0612/Excel-Killer-E-Learning-App)

![Excel killer]( https://excel-killer-images.s3.amazonaws.com/ex-logo.png)
Excel Killer is an open source learning application which strives towards helping users struggling with using MS Excel. It teaches python based Pandas for handling large set of data and Matplotlib for data visualisation. It covers four topics:
- Basics of Pandas
- Understanding the data
- Cleaning the data
- Data Visualisation

## Accessibility

A user can access the activities either through Excel Killer App directly or through NUS ALSET Achievements platform. 
![IMAGE ALT TEXT HERE]( https://excel-killer-images.s3.amazonaws.com/arch2.png )

## Developer Guide

#### Architecture:
Each of the above 4 activities are deployed as a standalone, stateless application on AWS Lambda connected to AWS Dynamo DB.

![IMAGE ALT TEXT HERE](https://excel-killer-images.s3.amazonaws.com/arch.png)

#### Deployment:
We support two ways for continuous integration and delivery which can automate the task of deployment. A developer can either use Travis CI or Github Workflow.
New developers do not have to take care of deploying things, they can simply push the code to Github. Below is the flow for smooth deployment:

- Developer pushes the code
- Travis CI/CD tool gets triggered
- Travis checkouts latest code from the repository
- It then builds and packages it
- Uploads the build on S3
- Lambda function takes the build from S3 and deploys it

 A developer just needs to take care of the environment variables which will be the developer's AWS credentials.

![IMAGE ALT TEXT HERE](https://excel-killer-images.s3.amazonaws.com/deploymentPipeline.png)

## License
>You can check out the full license [here](https://github.com/anshu0612/Excel-Killer-E-Learning-App/blob/master/LICENSE)

This project is licensed under the terms of the **MIT** license.
