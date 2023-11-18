import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node source-merchant. Replace with the appropriate bucket name.
pipersourcemerchant_node1695520980007 = glueContext.create_dynamic_frame.from_options(
    format_options={
        "quoteChar": '"',
        "withHeader": True,
        "separator": ",",
        "optimizePerformance": False,
    },
    connection_type="s3",
    format="csv",
    connection_options={"paths": ["s3://REPLACE-WITH-SOURCE-MERCHANT-BUCKET-NAME"], "recurse": True},
    transformation_ctx="pipersourcemerchant_node1695520980007",
)

# Script generated for node source-raw. Replace with the appropriate bucket name.
piperrawsource_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={
        "quoteChar": '"',
        "withHeader": True,
        "separator": ",",
        "optimizePerformance": False,
    },
    connection_type="s3",
    format="csv",
    connection_options={"paths": ["s3://REPLACE-WITH-SOURCE-RAW-NAME"], "recurse": True},
    transformation_ctx="piperrawsource_node1",
)

# Script generated for node Join Raw and Merchant Data
piperrawsource_node1DF = piperrawsource_node1.toDF()
pipersourcemerchant_node1695520980007DF = pipersourcemerchant_node1695520980007.toDF()
PiperJoinRawandMerchantData_node1695521076893 = DynamicFrame.fromDF(
    piperrawsource_node1DF.join(
        pipersourcemerchant_node1695520980007DF,
        (
            piperrawsource_node1DF["MerchantId"]
            == pipersourcemerchant_node1695520980007DF["MerchantIdentifier"]
        ),
        "left",
    ),
    glueContext,
    "PiperJoinRawandMerchantData_node1695521076893",
)

# Script generated for node Apply Mapping
ApplyMapping_node1695521180294 = ApplyMapping.apply(
    frame=PiperJoinRawandMerchantData_node1695521076893,
    mappings=[
        ("TransactionId", "string", "TransactionId", "string"),
        ("TransactionDate", "string", "TransactionDate", "string"),
        ("Amount", "string", "Amount", "string"),
        ("MerchantId", "string", "MerchantId", "string"),
        ("SKU", "string", "SKU", "string"),
        ("MerchantIdentifier", "string", "MerchantIdentifier", "string"),
        ("MerchantCity", "string", "MerchantCity", "string"),
        ("MerchantState", "string", "MerchantState", "string"),
        ("Zip", "string", "Zip", "string"),
        ("MerchantCategoryCode", "string", "MerchantCategoryCode", "string"),
    ],
    transformation_ctx="ApplyMapping_node1695521180294",
)

# Script generated for node Target/Transformed Data. Replace with the appropriate bucket name.
PiperTransformedData_node2 = glueContext.write_dynamic_frame.from_options(
    frame=ApplyMapping_node1695521180294,
    connection_type="s3",
    format="csv",
    connection_options={"path": "s3://REPLACE-WITH-TARGET-BUCKET-NAME", "partitionKeys": []},
    transformation_ctx="PiperTransformedData_node2",
)

job.commit()
