# Inspired by:
- https://www.youtube.com/watch?v=B0TJC4lmzEM
- https://inference-docs.cerebras.ai/cookbook/agents/sales-agent-cerebras-livekit
- https://github.com/livekit/agents?tab=readme-ov-file#simple-voice-agent
- https://inference-docs.cerebras.ai/cookbook/agents/build-your-own-perplexity#step-1:-environment-setup

## Voice Agendt architecture:
### User speech input:
VAD -> STT -> EOU
### Thinking phase:
LLM+Tools+Context
### Speaking phase
TTS: Text to speach model

VAD: vocie active detection model (filters all audio which is not speech(noice))
STT:  Speech-to-Text recognition model
EOU: End of utterance(or endo of speech) model allow to not interupt user by model

## Local env:
### Create virtual environment python3 -m venv .venv
### Activate virtual env.
source .venv/bin/activate
### Deactivate virtual env.
deactivate
### Check which python
.venv/bin/python
### Install pip 
python3 -m pip install --upgrade pip
python3 -m pip --version
### Create requirements file:
python pip freeze > requirements.txt
### Install requirements 
curl -sSL https://get.livekit.io/cli | bash
sudo apt-get install libportaudio2
python -m pip install -r requirements.txt

### Run local http://127.0.0.1:8000/
python manage.py runserver

### Run cli voice agent:
python chat/management/commands/voice_agent_command.py console   
### Run voice product manager(context avare)
python ./chat/management/commands/voice_product_expert.py console
### Run deep research assistant that can search web, analyzes multiple sources, and provide structured insights
python3 webUI/chat/management/commands/text_research_expert.py --query="best gift on New Year"
### 



### Tools
- livekit-cli for dev env.
- cloud.cerebras.ai as AI provider of fastes AI communication with AI(LLM) 50x time faster
- cartesia.ai for fastest Voice AI STT/TTS
- Exa API: The fastest search API engine for AI
### Packages 
- python-dotenv for work with env
- django for web ui
- livekit for real-time media application (Call rooms and etc.)