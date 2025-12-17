import json
import logging
import os
import redis

logger = logging.getLogger(__name__)

def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"Config file {file_path} not found")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse config file {file_path}: {e}")
        return {}

def connect_to_redis(config):
    try:
        return redis.Redis(host=config['host'], port=config['port'], db=config['db'])
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        return None

def get_config_from_redis(redis_client, key):
    try:
        return redis_client.get(key)
    except redis.ConnectionError as e:
        logger.error(f"Failed to retrieve config from Redis: {e}")
        return None

def save_config_to_redis(redis_client, key, config):
    try:
        redis_client.set(key, json.dumps(config))
    except redis.ConnectionError as e:
        logger.error(f"Failed to save config to Redis: {e}")

def main():
    config_file_path = os.environ.get('CONFIG_FILE_PATH', 'config.json')
    config = load_config(config_file_path)
    redis_client = connect_to_redis(config['redis'])
    if redis_client:
        key = config['key']
        redis_config = get_config_from_redis(redis_client, key)
        if redis_config:
            print(redis_config.decode('utf-8'))
        else:
            save_config_to_redis(redis_client, key, config)

if __name__ == '__main__':
    main()