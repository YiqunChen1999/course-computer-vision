
from cv.utilities.configs import Configs
import os
import sys
import yaml
import pytest
sys.path.append(__file__.replace("test/utilities/test_env.py", ""))
from cv.utilities.env import overwrite_configs_from_yaml

@pytest.mark.asyncio
def test_overwrite_from_yaml() -> Configs:
    configs = Configs(image=Configs())
    configs.general = Configs()
    ROOT = __file__.replace("test/utilities/test_env.py", "")
    configs.general.root = ROOT

    configs.image.type = ["png", "jpg", "jpeg"]
    # configs.segmentation.method = "threshold"
    configs.segmentation = Configs()
    configs.segmentation.method = " " #"local_threshold"
    configs.segmentation.threshold = Configs()
    configs.segmentation.threshold.bins = 20000
    configs.segmentation.threshold.thre = " "
    configs.segmentation.threshold.patches = (40, 40) # (num_rows, num_cols)
    configs.segmentation.meanshift = Configs()
    configs.segmentation.meanshift.kernel = "Gaussian"
    configs.segmentation.meanshift.bandwidth = 40
    configs.segmentation.meanshift.bins = 100
    configs.segmentation.meanshift.tolerance = 1
    configs.segmentation.meanshift.max_iters = 4000
    configs.segmentation.meanshift.patches = (40, 40) # (num_rows, num_cols)

    path2yaml = os.path.join(
        configs.general.root, "configs", "default.yml"
    )
    with open(path2yaml, 'r') as fp:
        configs_yaml = yaml.load(fp, yaml.Loader)["configs"]
    assert "segmentation" in configs_yaml.keys(), configs_yaml
    # configs = configs.cvt2dict()
    # configs.update(configs_yaml)
    # configs = Configs(configs)
    configs = overwrite_configs_from_yaml(configs, path2yaml)
    configs.cvt_state(read_only=True)
    configs_yaml = Configs(configs_yaml)
    assert configs.segmentation.meanshift.kernel == "Gaussian"
    assert configs.general.root == ROOT, configs.general.root
    assert configs.segmentation.meanshift.bins == 10
    assert configs.segmentation.method == \
            configs_yaml.segmentation.method
    for item in configs.segmentation.threshold.keys():
        assert configs.segmentation.threshold[item] == \
            configs_yaml.segmentation.threshold[item]
    for item in configs_yaml.segmentation.meanshift.keys():
        assert configs.segmentation.meanshift[item] == \
            configs_yaml.segmentation.meanshift[item]
    return configs
