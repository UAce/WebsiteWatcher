import toml
import os

# Read toml file
env = os.getenv("ENVIRONMENT", "development")
settings_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = f"{settings_dir}/{env}.toml"
config = toml.load(config_file_path)

# Retrieving a dictionary of values
config["project"]
config.get("project")

# Get email info
email_api_key = os.getenv("EMAIL_API_KEY", config["email"]["api_key"])
email_sender = os.getenv("EMAIL_SENDER", config["email"]["sender"])
email_recipients = os.getenv("EMAIL_RECIPIENTS", config["email"]["recipients"]).split(",")
