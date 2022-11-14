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
