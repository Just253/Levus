from worker import update_status

def process_interaction(user_input, process_id):
    response = call_openai(user_input)
    if response.get('command'):
        execute_command(response['command'], process_id)
    else:
        update_status(process_id, "completed", response=response['text'])

def call_openai(user_input):
    import openai
    openai.api_key = 'YOUR_OPENAI_API_KEY'
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=150
    )
    return response.choices[0].text

def execute_command(command, process_id):
    from command import run_command
    result = run_command(command)
    if result['success']:
        update_status(process_id, "completed", response=result['output'])
    else:
        update_status(process_id, "error", error=result['error'])
