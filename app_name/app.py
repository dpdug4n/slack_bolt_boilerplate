import os, re, logging, json, sys, string

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
#custom functions
from utils.helpers import example_function, channel_map, set_messages
#for importing env vars from file 
from dotenv import load_dotenv

#starts with xapp - Basic Information > App-Level Tokens in Slack App UI (https://api.slack.com/apps)
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
# starts with xoxb - OAuth & Permissions > Bot User OAuth Token in Slack App UI
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
# starts with xoxp - OAuth & Permissions > User OAuth Token in Slack App UI
SLACK_USER_TOKEN = os.getenv("SLACK_USER_TOKEN")

load_dotenv() #load from .env & set tokens. Comment out when using portainer, docker-compose, or AWS task definitions to import env vars

#init vars for filepaths
dirname = os.path.dirname(__file__)
#load views from json file
viewspath = os.path.join(dirname, 'assets/views.json')
with open(viewspath,'r') as f:
    views = json.load(f) 

# Initializes your app with your bot token and socket mode handler
app = App(token=SLACK_BOT_TOKEN)

# map channel names to IDs
_channels = channel_map(app)

### Logger ###
#send logs to stdout for docker logging/cloudwatch/ecs-fargate
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)]
)




### Shortcuts ###
#https://slack.dev/bolt-python/concepts#shortcuts

## Example Shortcut 
@app.shortcut("example_shortcut")
def open_exmaple_modal(ack, body, client, logger):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view=views['support_case']
    )
    logger.info(f"{body['user']['username']} opened the example modal.")
@app.view("example_view") #this is the callback ID of the modal's json
def handle_example_submission(ack, body, view, logger, say):
    user = body['user']['username']
    params = {
        "input1" : view['state']['values']['input1_block']['input1_action']['value'],
        "input2" : view['state']['values']['input2_block']['input2_action']['value'],
    }
    #input validation
    errors = {}
    for field in params.keys(): 
        if len(params[field]) > 3000:
            errors[f'{field}_block']='Max character limit is 3k.' 
    if len(errors) > 0:
        ack(response_action="errors",errors=errors)
        return
    messages=['*Response form*\n']
    for k,v in params.items():
        k=string.capwords(k.replace('_',' '))
        msg = f"{k}:\n```{v}```\n"
        messages.append(msg)
    msg = set_messages(user, messages)

    try:
        say(blocks=msg, 
            text=f"{user} posted an example form to CHANNEL", 
            channel='CHANNEL',
            unfurl_links=False)
        logger.info(f"{user} posted an example form to CHANNEL")
    except Exception as e:
        logger.error(f"Failed to post a message {e}")

### Quick Commands ###
@app.command('/example_command')
def example_command(ack, respond, command, body, logger):
    ack()
    response = example_function(command['text'])
    respond(response)
    logger.info(f"{body['user_name']} called example command and recived the following output:\n{response}")


### Message Listeners ###
@app.event({"type":"message"})
def message_handler(client, message, logger):
    if message['channel'] == _channels['channel_name']:
        pass #call a channel dependent function here

# Start the app in socket mode
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()