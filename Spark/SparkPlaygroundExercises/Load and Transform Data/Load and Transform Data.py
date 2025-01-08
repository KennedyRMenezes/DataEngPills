from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('Spark Playground').getOrCreate()

file_path = '/datasets/customers.csv'

df = spark.read.format('csv').option('header', 'true').load(file_path)

df = df.filter('age >= 30')
df = df.filter('purchase_amount > 100')
df = df.select(['customer_id', 'name', 'purchase_amount'])

# IN ONE LINE
#df = df.filter('age >= 30 and purchase_amount > 100').select(['customer_id', 'name', 'purchase_amount'])

display(df)