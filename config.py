import toml
import os

# Read local `config.toml` file
config_file_path = 'config/config.toml'
config = toml.load(config_file_path)

# Retrieving a dictionary of values
config['project']
config.get('project')

# Retrieving a value
config['project']['author']
config.get('project').get('author')
email_api_key = os.getenv('EMAIL_API_KEY', config['email']['api_key'])
email_sender = os.getenv('EMAIL_SENDER', config['email']['sender'])
email_recipient = os.getenv('EMAIL_RECIPIENT', config['email']['recipient'])
