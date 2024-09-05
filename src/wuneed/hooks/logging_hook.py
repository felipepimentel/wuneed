from wuneed.utils.hook_manager import hook_manager
import logging

def log_command(command: str, *args, **kwargs):
    logging.info(f"Command executed: {command} with args: {args} and kwargs: {kwargs}")

def register_hooks(manager):
    manager.register_hook("pre_command", log_command)