import os, sys
import django
from livekit.plugins import openai, silero, cartesia
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    RunContext,
    WorkerOptions,
    cli,
    function_tool,
)
import logging

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from chat.services.product_context_service import ProductContextLoaderService
from chat.services.sales_agent import VoiceSalesAgent
# service_directory_path = os.path.abspath('chat/services')
# sys.path.insert(0, service_directory_path)

# from service_directory_path import ProductContextLoaderService

# from django.core.management.base import BaseCommand

# class VoiceAgentCommand(BaseCommand):
# class Command(BaseCommand):
#     help = 'Run voice AI agent from the CLI'

#     def add_arguments(self, parser):
#         parser.add_argument('user_name', type=str, help='The user name to greet')
#     def handle(self, *args, **kwargs):
#         user_name = kwargs['user_name']
#         self.stdout.write(self.style.SUCCESS(f"Hello, {user_name}!"))
#         self.stdout.write('Init AI AGET in CLI mode...')

async def product_agent_entrypoint(ctx: JobContext):
    # logger = logging.getLogger(__name__)
    voice_agent = VoiceSalesAgent()
    session = AgentSession()
    # await session.start(room=ctx.room, agent=agent)
    await session.start(room=ctx.room, agent=voice_agent)
  



if __name__ == '__main__':
    # Setup environ
    # sys.path.append(os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webUI.settings")
    # Setup django
    django.setup()
    # Run livekit in CLI mode
    cli.run_app(WorkerOptions(entrypoint_fnc=product_agent_entrypoint))