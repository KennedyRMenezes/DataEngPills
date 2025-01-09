# Initialize Spark session
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
spark = SparkSession.builder.appName('Spark Playground').getOrCreate()

#enter the file path here
file_path = "/datasets/customer_purchases.csv"

#read the file
df = spark.read.format('csv').option('header', 'true').load(file_path)

df = df.groupBy('customer_id').agg({'purchase_amount': 'sum'}).orderBy('customer_id')
df = df.withColumnRenamed('sum(purchase_amount)', 'total_purchase')
df = df.withColumn('total_purchase', col('total_purchase').cast('int'))

# Display the final DataFrame using the display() function.
display(df)