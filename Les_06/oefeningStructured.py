
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, current_timestamp, window, col

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
    explode(split(lines.value, ' ')).alias('word'),
    current_timestamp().alias('timestamp')
)

words = words.withWatermark('timestamp', '1 minute')

# maak windows van 5 seconden aan
counts = words.groupby( # group by op 2 niveaus, eerste niveau is per window dan per woord
    window(words.timestamp, '5 seconds', '1 seconds'), 
    words.word).count()

# maak de output iets duidelijker -> haal start en eindtijstip uit de window kolom
counts = counts.withColumn('window_start', col('window.start')) \
    .withColumn('window_end', col('window.end')) \
    .drop('window')

# naar waar moet de streaming data?
#query = counts.writeStream \
#    .outputMode('update') \
#    .format('console') \
#    .start()
# complete outputmode: anders krijg je een error die zegt dat append niet ondersteund wordt bij groupby

#query.awaitTermination()

output_path = 's3a://04-streaming/output'
query_csv = counts.writeStream \
    .outputMode('append') \
    .format('csv') \
    .option('path', output_path) \
    .option('checkpointLocation', output_path + '_checkpoints') \
    .start()
query_csv.awaitTermination()
