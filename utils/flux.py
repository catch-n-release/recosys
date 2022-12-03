# from prefect import task
# import tomli as toml
# import pandas as pd
# from deepchecks.tabular import Dataset
# from datetime import timedelta
# from omegaconf import OmegaConf
# from prefect.tasks import task_input_hash

# @task
# def boot_config() -> type:
#     try:
#         with open("pyproject.toml", "rb") as stream:
#             toml_dict = toml.load(stream)
#         config = OmegaConf.create(toml_dict)
#         return config
#     except Exception as e:
#         raise e

# @task
# def sift_success(result) -> bool:
#     try:
#         assert result.passed()
#     except Exception as e:
#         raise e

# @task(
#     cache_key_fn=task_input_hash,
#     cache_expiration=timedelta(days=1),
# )
# def boot_dc_dataset(
#     data: pd.DataFrame,
#     config,
# ):
#     try:
#         return Dataset(
#             data,
#             cat_features=list(config.app.ml.data.categorical_columns),
#             label=config.app.ml.data.label,
#             label_type=config.app.ml.data.label_type,
#         )
#     except Exception as e:
#         raise e

# @task
# def boot_train_test(config: OmegaConf) -> dict:
#     try:
#         datasets = {
#             str(config.app.ml.const.trainset):
#             pd.read_csv(config.app.path.trainset),
#             str(config.app.ml.const.testset):
#             pd.read_csv(config.app.path.testset),
#         }

#         return datasets

#     except Exception as e:
#         raise e
