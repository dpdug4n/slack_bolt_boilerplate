# include your general utility functions/modules here and import them in your app.py 
# this helps keep the code clean and organized. You can also create additional .py modules in this folder to further organize your project.

def example_function(input):
    return (str(input))


def channel_map(app):
    channels = {}
    channel_list = app.client.conversations_list(exclude_archived=True,limit=100)
    if channel_list['response_metadata']['next_cursor'] != '':
        more_pages = True
        while more_pages:
            cursor = channel_list['response_metadata']['next_cursor']
            for channel in channel_list['channels']:
                channels[channel['name']]=channel['id']
            if cursor == '':
                more_pages = False
            channel_list = app.client.conversations_list(exclude_archived=True,limit=100, cursor=cursor)
    else:
        for channel in channel_list['channels']:
            channels[channel['name']]=channel['id']
    return channels

def set_messages(user, messages):
    message_blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<@{user}>"
                }
            }
        ]
    for message in messages:
        block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{message}"
                }
            }
        message_blocks.append(block)

    return message_blocks