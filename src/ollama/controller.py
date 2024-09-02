import json
from pprint import pprint

import ollama
# this script will have the top level functions related to ollama


entry_annotation_prompt = """\
You are responsible for taking in thoughts throughout the day, and creating an outline for
what the user plans to do and ends up doing throughout the day. Your output shall only be
in json format for the "response" interface, defined by the following typescript-style 
schema: 

interface response {{
    tasks?: task[];
    actions?: action[];
}}

interface task {{
    text: string; // a concise string representing the task
    parentId?: number; // a number matching the id of the parent task it relates to
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
    taskId: number; // a number matching the id of the parent task it relates to. This cannot be any of the tasks returned, as those will automatically have a "create" action assigned to them. 
}}


Your responses also must follow these rules: 
1) no hallucination or creativity. You are responsible for taking the words I give and giving them structure, not for extrapolation. For example: if an entry says "I need to polish my coding project", you should respond with a single structured task "polish coding project". you should NOT respond with the "polish coding project" task with children "create documentation" and "fill out tests". If I wanted that in the response the entry would be "I need to polish my coding project by creating documentation and filling out tests". Then, the nested response would be acceptable
2) start time is occasionally okay to guess, but only when time is mentioned in the entry. For example if I say "I should mow the lawn tomorrow morning", an 8am time for tomorrow morning can be attached, and I can change it around later. 
3) end time is okay to guess when there is a start time, but again that should only be if it's mentioned. If I say "tomorrow morning I should spend a little bit tidying the kitchen", a morning start time and a 20-minute-later end time would be okay, depending on how long a task like that should take.

And now to the prompt:

Given this context: 
{task}

Please consider this prompt:
{newEntry}

I would like for you to consider the task and nested subtasks shown and think of 
any sub-tasks this adds, as well any actions this might perform upon them out of 
the examples in the action_str enum.

"""

# for example, when the engine cycles it will be shown the context and the  
def process_entry(entry: dict, context: dict | list | None) -> dict:
    prompt = entry_annotation_prompt.format(
        task=json.dumps(context or "no context provided"),
        newEntry=json.dumps(entry)
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
        task=json.dumps(context or "no context provided"),
        newEntry=json.dumps(entry)
    )

    prompt = entry_correction_prompt.format(
        original_prompt=original_prompt,
        response=json.dumps(original_response),
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
    


