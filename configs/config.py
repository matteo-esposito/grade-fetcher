import yaml

with open("configs/globalcfg.yaml", 'r') as yaml_file:
    cfg = yaml.safe_load(yaml_file)
