import toml

# Read local `config.toml` file
config_file_path = 'config/config.toml'
config = toml.load(config_file_path)

# Retrieving a dictionary of values
config['project']
config.get('project')

# Retrieving a value
config['project']['author']
config.get('project').get('author')
