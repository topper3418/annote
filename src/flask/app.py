# this will allow for simple interactions with the app over a restful interface


# get / gives the currently focused task
#   allows to see parent
#   allows to see unfocused siblings

# thats the old one above
# GET / -> all top level tasks, as objects populated with minimal stuff
# GET /:taskid -> gets the details for a task, can be big if a top level task
# GET /entries -> gets the entries in current focus scope
# GET /entries/:entryid -> gets the metadata for the entry
# POST / -> create an entry
# POST /command -> post specifically a command


# post / allows you to create entries
