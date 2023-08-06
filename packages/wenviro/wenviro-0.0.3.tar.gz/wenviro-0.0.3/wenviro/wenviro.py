import configparser
import os

class Wenviro(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(os.environ.get('ENV_FILE'))
        self.env = os.environ.get('ENV')

    def get_env_var(self, key):
        try:
            env_value = self.config.get(self.env, key)
        except configparser.NoOptionError:
            if not os.environ.get(key):
                raise WenviroException("No existe "+key)
            env_value = os.environ.get(key)
        
        return env_value

class WenviroException (Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return "No existe :"+self.value