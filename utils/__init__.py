from omegaconf import OmegaConf
import tomli as toml
# with open("pyproject.toml", "rb") as stream:
#     toml_dict = toml.load(stream)
# app_config = OmegaConf.create(toml_dict)

# from utils.logger import Logger

# log = Logger(toml_file_path=app_config.app.path.self).setup()

from utils.testing import DeepchecksModelWrapper
# from utils.flux import boot_config, sift_success, boot_dc_dataset, boot_train_test
