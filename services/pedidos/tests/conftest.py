## tests\conftest.py
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=".env.test", override=True)

os.environ['ENV'] = 'test'

def pytest_configure(config):
  env_file = find_dotenv('src./.env.test')
  load_dotenv(env_file)
  return config

  