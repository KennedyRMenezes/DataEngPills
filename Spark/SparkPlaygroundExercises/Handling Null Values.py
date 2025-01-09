# Initialize Spark session
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('Spark Playground').getOrCreate()

#enter the file path here
file_path = "/datasets/customers_raw.csv"

#read the file
df = spark.read.format('csv').option('header', 'true').load(file_path)

df = df.na.drop()

# Display the final DataFrame using the display() function.
display(df)