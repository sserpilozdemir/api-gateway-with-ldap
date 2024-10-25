import yaml


class Config:
    def __init__(self, file_path):
        self.config = self.load_config(file_path)

    def load_config(self, file_path):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    def get(self, path, default=None):
        keys = path.split('.')
        value = self.config
        for key in keys:
            value = value.get(key, default)
            if value == default:
                break
        return value

config = Config('config.yaml')
