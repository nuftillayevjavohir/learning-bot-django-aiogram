from core.asgi import application  # noqa

import os
import environ
from pathlib import Path


# READING ENV
base_dir = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
env.read_env(os.path.join(base_dir, ".env"))

# GETTING WEBHOOK URL
webhook_path = '/telegram-bot/webhook/'
webhook_url = f"{env.str('BASE_URL', 'https://learning.jprq.app')}{webhook_path}"
