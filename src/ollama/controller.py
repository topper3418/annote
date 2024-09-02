import json
from pprint import pprint

import ollama
# this script will have the top level functions related to ollama


entry_annotation_prompt = """\
You are responsible for taking in thoughts throughout the day, and creating an outline for
what the user plans to do and ends up doing throughout the day. Your output shall only be
in json format for the "response" interface, defined by the following typescript-style 
schema: 

// this is the object you will return each time
interface response {{
    tasks?: task[];
    actions?: action[];
}}

interface task {{
    text: string; // a concise string representing the task
    parentName?: string; // the name of the task that is the parent of this one, if applicable.
    start?: string; // string in the format of "%m/%d/%y %H:%M" estimating the start time of the task
    end?: string; // string in the format of "%m/%d/%y %H:%M" estimating the end time of the task,
    children?: task[]; // a list of subtasks, if applicable. same shape as this task object, but parentId will be implied so do not include it
    focus: boolean; // does this seem like something the user intends to put effort or thought into in the immediate future?
}}    

enum action_str {{
    begin = "begin",
    pause = "pause",
    complete = "complete",
    cancel = "cancel",
    note = "note"
}}

interface action {{
    action: action_str; // what does this entry seem to do to this task?
    taskName: string; // a string matching the name of the parent task it relates to. This cannot be any of the tasks returned, as those will automatically have a "create" action assigned to them. 
}}


Your responses also must follow these rules: 

1) if a time is not mentioned, do not provide a time or a time estimate for a task created
2) do not repeat back any tasks that are already given in the context. 
3) do not extrapolate beyond what is given in each entry. your job is cleanup and organization, not inference. 
4) you must never pass a "create" action.


This is the json-formatted context upon which the user is submitting their entry. They may or may not have this data in front of them displayed on a webapp: 

{task}

This is the json-formatted journal entry:

{newEntry}

I would like for you to consider that entry in the context of the nested list of tasks and subtasks, and decide if the entry adds context or takes any action upon any of them. 
Please respond in only json, and only in the format provided above. 

"""

# for example, when the engine cycles it will be shown the context and the  
def process_entry(entry: dict, context: dict | list | None) -> dict:
    prompt = entry_annotation_prompt.format(
        task=json.dumps(context or "no context provided", indent=4),
        newEntry=json.dumps(entry, indent=4)
    )
    print("PROMPTING")
    print(prompt)
    response = ollama.generate(
        prompt=prompt,
        format='json',
        model='llama3.1',
        options={ 'temperature': 0 },
        stream=False
    )

    parsed_response = json.loads(response['response'])
    print("\nRESPONSE")
    pprint(parsed_response)
    return parsed_response

entry_correction_prompt = """
you previously responded to the following prompt in a way that caused an error: 

############################# Original Prompt ################################

{original_prompt}

######################### End of Original Prompt #############################

your response was:

{response}

Unfortunately, this response resulted in the following error: 

{error}

Please try to address the error by generating a corrected response
"""


def attempt_to_fix_entry_processing(entry: dict, 
                                    context: dict | list | None,
                                    original_response: dict,
                                    original_error: str) -> dict:
    original_prompt = entry_annotation_prompt.format(
        task=json.dumps(context or "no context provided", indent=4),
        newEntry=json.dumps(entry, indent=4)
    )

    prompt = entry_correction_prompt.format(
        original_prompt=original_prompt,
        response=json.dumps(original_response, indent=4),
        error=original_error
    )

    print("PROMPTING")
    print(prompt)
    response = ollama.generate(
        prompt=prompt,
        format='json',
        model='llama3.1',
        options={ 'temperature': 0 },
        stream=False
    )

    parsed_response = json.loads(response['response'])
    print("\nRESPONSE")
    pprint(parsed_response)
    return parsed_response
    


