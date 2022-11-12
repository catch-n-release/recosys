from datetime import timedelta
import pandas as pd
from prefect import task
from prefect.tasks import task_input_hash


@task(
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(days=1),
)
def boot_dataframe(config: type) -> pd.DataFrame:
    try:
        return pd.read_csv(config.app.path.dataset)
    except Exception as e:
        raise e


# from kafka import KafkaConsumer
# import time
# import pandas as pd
# from ml import log

# class Ingress:

#     def __init__(
#         self,
#         topic: str = "movielog11",
#         bootstrap_servers: list = ["localhost:9092"],
#         auto_offset_reset: str = "earliest",
#         enable_auto_commit: bool = True,
#         auto_commit_interval_ms=1000,
#     ):

#         self.topic = topic
#         self.bootstrap_servers = bootstrap_servers
#         self.auto_offset_reset = auto_offset_reset
#         self.enable_auto_commit = enable_auto_commit
#         self.auto_commit_interval_ms = auto_commit_interval_ms

#     def consume(self) -> list:
#         try:
#             consumer = KafkaConsumer(
#                 self.topic,
#                 bootstrap_servers=self.bootstrap_servers,
#                 # Read from the start of the topic; Default is latest
#                 auto_offset_reset=self.auto_offset_reset,
#                 # Commit that an offset has been read
#                 enable_auto_commit=self.enable_auto_commit,
#                 # How often to tell Kafka, an offset has been read
#                 auto_commit_interval_ms=self.auto_commit_interval_ms,
#             )
#             ratings = []
#             log.info('Reading Kafka Broker')
#             for message in consumer:
#                 message = message.value.decode()
#                 movie_request = message.split(',')[2]
#                 movie_request_split = movie_request.split('/')
#                 if len(movie_request_split) > 2:
#                     if movie_request_split[1] == 'rate':
#                         ratings.append(message)
#                 if len(ratings) == 1000:
#                     break
#             return ratings

#         except Exception as e:
#             raise e

#     def ingest(
#         self,
#         csv_name: str = f"raw_data_{int((time.time())*1000)}.csv",
#     ) -> str:
#         try:
#             df = pd.DataFrame(self.consume(), columns=['event'])
#             df['timestamp'] = df.event.apply(lambda x: x.split(',')[0])
#             df['user_id'] = df.event.apply(lambda x: x.split(',')[1])
#             df['request'] = df.event.apply(lambda x: x.split(',')[2])
#             df['movie'] = df.request.apply(lambda x: x.split('/')[-1])
#             df['movie_name'] = df.movie.apply(lambda x: x.split('=')[0])
#             df['movie_rating'] = df.movie.apply(lambda x: x.split('=')[-1])
#             df['movie_year'] = df.movie_name.apply(lambda x: x.split('+')[-1])
#             df = df.drop(columns=['movie'])
#             df.to_csv(f'data/{csv_name}')
#             return csv_name
#         except Exception as e:
#             raise e
