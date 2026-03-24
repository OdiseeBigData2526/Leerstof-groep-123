from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split

# Create a local StreamingContext with two working thread and batch interval of 5 second
spark = SparkSession.builder \
    .appName("SparkMinIODemo") \
    .master("spark://spark-master:7077") \
    .config("spark.jars.packages", 
            "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.301") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio1:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "bigdata") \
    .config("spark.hadoop.fs.s3a.secret.key", "bigdata123") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()
    # voor studenten die problemen hebben met het connecteren van eu-west-1
   # .config("spark.hadoop.fs.s3a.endpoint.region", "eu-west-1") \

sc = spark.sparkContext
sc.setLogLevel("ERROR") # reduce spam of logging

# vanwaar komt ons streaming data
lines = spark.readStream \
    .format('socket') \
    .option('host', 'jupyterlab') \
    .option('port', 19999) \
    .load()

# verwerk de streaming data
words = lines.select(
    explode(split(lines.value, ' ')).alias('word')
)

counts = words.groupby('word').count()

# naar waar moet de streaming data?
query = counts.writeStream \
    .outputMode('complete') \
    .format('console') \
    .start()
# complete outputmode: anders krijg je een error die zegt dat append niet ondersteund wordt bij groupby

query.awaitTermination()
