# INITIAL PLAN
# The engine will be responsible for using ollama in the background
# First, it will search through tags and create associations for any
# that properly match. 
# Then, it will create tags and associate them with the note, if applicable.
# decide if the note is a task or not, create a task if it is.
# Next we look through active tasks and see if any of them are relevant to the note
# Next it will look through the last 100 keywords and decide if any of them are relevant. Filter to the top 10.
# are relevant to the note. If so, it will pull up the full note and create an association
# with a 1-10 strength.
# if any associations are strong enough it should assign that note as the parent. 
# if none are strong enough it should be a child of the task if one was found. 
# if no association is strong enough it will just be a note. 


# RETHINKING
# I will need a way to manually vet these all as well. I should be able to start a note with command: or com: and
# then it will register stuff differently. I can use this to activate a function manually. 
# flow would be: 
# user > command: create note "this is a note"
# engine > py > create_note("this is a note")
# engine >    > # approve? (y/n)
# user > y
# engine > Note(this is a note)
# another example: 
# user > command: create task "this is a task"
# engine > py > create_task("this is a task")
# engine >    > # approve? (y/n)
# user > y
# engine > Task(this is a task)
# another example:
# user > command: assign a due date to fixing my truck to tomorrow
# engine > py > assign_due_date(
# engine >    >     task=Task(fix truck),
# engine >    >     due_date=tomorrow
# engine >    > )
# engine >    > # approve? (y/n)
# user > y
# engine > Due date 05/18/25 assigned to Task(fix truck)


# ANOTHER ITERATION
# ok so I am now realizing that I should start this project as a cli-controlled note taking app
# > annote "this is a note"
# just creates a note
#
# > annote "this is a note" --task
# creates a note as a task
#
# > annote "a thought is something that I don't necessarily need to act on, I just wanted to take the time to write it down" --tag "thought"
# creates a tag with a name "thought" and a corresponding description. Tags will automatically be associated with notes
# upon creation
# 
# > annote "add the thought tag to my note about the birdfeeder" --command
# brings the function calling module up and displays the intended function call, and requests approval
#
# > annote "add the thought tag to my note about the birdfeeder" --command --approve
# executes the function call without checking for approval
#
# > annote "Fix Truck"
# creates a note
# > annote "convert the note about fixing the truck to a task" --command
# brings the function calling module up. should show everything I need to know thats being changed
# > annote "I need fo fix my truck by next friday" --command
# brings the function calling module up. demonstrates that the due date is being altered on the task and requests approval
# > annote "I need to get oil to fix my truck" --subtask
# creates a task with the raw note as the content. Ollama takes its best guess of what the parent is
# > annote "the oil subtask was actually supposed to be a child of the truck task" --command
# brings the function calling module up. shows that the parent is being changed and requests approval
# > annote "I got oil" --complete
# creates a "completion note" that is associated with the subtask