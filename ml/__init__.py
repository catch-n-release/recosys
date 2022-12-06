from omegaconf import OmegaConf
import tomli as toml
with open("ml/pyproject.toml", "rb") as stream:
    toml_dict = toml.load(stream)
app_config = OmegaConf.create(toml_dict)

from utils import Logger

log = Logger(toml_file_path=app_config.ml.path.self).setup()

# from ml.src.ingress import boot_dataframe
# from ml.src.preprocess import filter_columns
# from ml.src import sifts
# from ml.src.train import train
# from ml.src.preprocess import preprocess_dataset
# from ml.src.flux import init_flux
# from ml.utils import boot_config
