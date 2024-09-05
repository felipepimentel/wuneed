from wuneed.plugins.manager import wuneed_hook

@wuneed_hook('startup')
def hello_world():
    print("Hello, World! This is an example plugin.")

@wuneed_hook('command_executed')
def log_command(command: str):
    print(f"Command executed: {command}")