# Slack Boilerplate
## Docker 
 Execute `docker-compose --env-file ./app_name/.env up` to build and start the docker container.  
 `docker-compose --force-recreate && docker-compose up` to rebuild the container after making changes to app.py
## Tips
When your app uses blockkit views for home pages, shortcut modals, etc -  
store each view's JSON in `./assets/views.json` with the property as the view name, and the value as the view's json.  
 - The boilerplate loads this file and assigns it to a `views` variable, reference each view via `views['view_name']`  

To allow for dynamic parsing of views and their inputs, use a standard naming convention in the block ids and action ids.
- An input field named `user_input` would have a block id of `user_input_block` and the element's action id would be `user_input_action`
    ```
    params = {
        "input1" : view['state']['values']['input1_block']['input1_action']['value'],
        "input2" : view['state']['values']['input2_block']['input2_action']['value'],
    }
    #dynamic input validation
    errors = {}
    for field in params.keys(): 
        if len(params[field]) > 3000:
            errors[f'{field}_block']='Max character limit is 3k.' 
    if len(errors) > 0:
        ack(response_action="errors",errors=errors)
        return
    ```

Store utility functions in `./utils/helpers.py` or in their own .py modules and import them into app.py
- This helps keep the code clean & organized and helps prevent the application code from being monolithic.
- Add an empty `__init__.py` file in a subfolder to enable python to recognize it as a module and import the submodules.

Rename .env.example to .env if you're using it for local development.

## Useful Links
- https://api.slack.com/apps
- https://slack.dev/bolt-python/tutorial/getting-started
- https://app.slack.com/block-kit-builder/
- https://api.slack.com/reference/surfaces/formatting
- https://api.slack.com/methods
- https://slack.dev/bolt-python/api-docs/slack_bolt/