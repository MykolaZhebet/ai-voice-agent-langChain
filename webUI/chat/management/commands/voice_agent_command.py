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

@function_tool
async def lookup_weather(
    context: RunContext,
    location: str,
):
    """Used to look up weather information."""

    return {"weather": "sunny", "temperature": 70}

async def simple_voice_entrypoint(ctx: JobContext):
# from livekit.plugins import deepgram, elevenlabs, openai, silero
    #Inspired @see by https://github.com/livekit/agents?tab=readme-ov-file#simple-voice-agent
    await ctx.connect()

    agent = Agent(
        instructions="You are a friendly voice assistant built by LiveKit.",
        tools=[lookup_weather],
    )
    session = AgentSession(
        # vad=silero.VAD.load(),
        # any combination of STT, LLM, TTS, or realtime API can be used
        # stt=deepgram.STT(model="nova-3"),
        # llm=openai.LLM(model="gpt-4o-mini"),
        # tts=elevenlabs.TTS(),
        vad = silero.VAD.load(),# voice activity detection
        llm = openai.LLM.with_cerebras(model='llama-3.3-70b'),
        stt = cartesia.STT(),#  for realtime speech to text
        tts = cartesia.TTS(),# for text to speech    
    )

    await session.start(agent=agent, room=ctx.room)
    await session.generate_reply(instructions="greet the user and ask about their day")



if __name__ == '__main__':
    # Setup environ
    sys.path.append(os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webUI.settings")

    # Setup django
    
    django.setup()
    cli.run_app(WorkerOptions(entrypoint_fnc=simple_voice_entrypoint))


    # now you can import your ORM models 