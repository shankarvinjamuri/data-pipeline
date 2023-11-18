## Overview
This repository covers a methodology for combining and processing multiple datasets. It covers three stages:
1. Data ingestion into Amazon S3.
2. Transformation of source datasets into a target format using AWS Glue.
3. Storage back to Amazon S3 of the combined data sets.

## Architecture
![Alt text](/architecture/DataProcessor.png)

## Tools and Technologies
- Amazon S3
- Amazon EventBridge
- AWS Lambda
- AWS Glue

## Prerequisites
1. Ensure you have an active AWS Account
2. Create a unique bucket and record the name. This name serves as an input parameter (GlueScriptsBucketName) in the CloudFormation template.
3. Once the bucket is created, copy the file "glue-etl-script.py" into it. You can find this file in the "/scripts" folder.
3. Confirm the availability of the files "merchants.csv" and "receiptdata.csv." These sample data files can be found in the "/source-data" folder. You are welcome to modify the data content as needed, but please refrain from altering the header fields in the CSV files.

## How to run AWS CloudFormation stack?
The "data-processor.yaml" file located in the "/cloud-formation" folder contains the essential Infrastructure as Code (IAC) instructions to create the required AWS resources. Here is an overview:
1. Creates the necessary IAM roles.
2. Creates Lambda function.
3. Creates AWS Glue job that loads the script from a S3 bucket, which was created as part of the prerequisites outlined earlier.
4. Creates EventBridge rule.
5. Creates the source and target buckets.

### Update the bucket names in the Glue job script
1. Access the Glue job service from the AWS management console.
2. Click on the glue job (acpy-glue-job) that was created as part of the CloudFormation stack.
3. Edit the â€˜Scriptsâ€™ tab, and replace the bucket names that were created as part of CloudFormation stack
    s3://REPLACE-WITH-SOURCE-MERCHANT-BUCKET-NAME" with SourceMerchantBucketName value.
    s3://REPLACE-WITH-SOURCE-RAW-NAME" with SourceRawBucketName value.
    s3://REPLACE-WITH-TARGET-BUCKET-NAME" with TargetBucketName value.
4. Click â€˜Saveâ€™.

## Validation
1. The source data sets include two sample files - "merchants.csv" and "receiptdata.csv,", can be found in the "/source-data" folder.
2. Copy these files to the respective S3 buckets that are created as part of the CloudFormation run:
    - Copy merchants.csv into 'SORUCE-MERCHANT-BUCKET'
    - Copy receiptdata.csv into 'SORUCE-RAW-BUCKET'
3. Upon successful upload of "receiptdata.csv" to the 'SORUCE-RAW-BUCKET' bucket, AWS EventBridge rule will be triggered automatically. This rule will invoke the Lambda function, leading to the execution of the associated Glue job, responsible for transforming the CSV file into its target state.
4. Please feel free to examine the 'run details' of the AWS Glue job. The transformation may require up to 2 minutes to be fully executed.
5. Refer to the 'TARGET-BUCKET' bucket to access the output file.
6. Repeat the process by updating either the "merchants.csv" or "receiptdata.csv" files as required.

## Cleanup
1. After completing the validations, make sure to empty the S3 buckets that were created as part of the CloudFormation stack. This step helps in maintaining data cleanliness and avoiding any unintentional data retention.
2. If necessary, delete the CloudFormation stack to release AWS resources.