import React, { useEffect, useState } from 'react'
import './App.css'

import useGetTasks from './hooks/getTasks';
import useGetEntries from './hooks/getEntries';
import { TaskCard } from './components/taskCard';
import { EntryCard } from './components/entryCard';



function App() {
  const { tasks, loading: tasksLoading, error: tasksError, refetch: tasksRefetch } = useGetTasks();
  const { entries, loading: entriesLoading, error: entriesError, refetch: entriesRefetch } = useGetEntries();
  const [expandedTaskId, setExpandedTaskId] = useState<number | null>(null);
  const [selectedEntryId, setSelectedEntryId] = useState<number | null>(null);

  if (tasksLoading) console.log("loading tasks...");
  if (tasksError) console.error("error loading tasks: ", tasksError);
  if (entriesLoading) console.log("loading entries...");
  if (entriesError) console.error("error loading entries: ", entriesError);
  if (entries) console.log("entries: ", entries);

  useEffect(() => {
    console.log(`task id ${expandedTaskId} selected`)
  }, [expandedTaskId])

  return (

    <div className="column padded">
      <h1>Annote</h1>
      <div className="row spaced">
        <div className="column repeater width-60 padded">
          <h3 onClick={tasksRefetch}>Tasks</h3>
          {tasks && tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              expandedId={expandedTaskId}
              setExpandedId={setExpandedTaskId} />
          ))}
        </div>
        <div className="column repeater width-40 padded">
          <h3 onClick={entriesRefetch}>Entries</h3>
          {entries && entries.map((entry) => (
            <EntryCard
              key={entry.id}
              entry={entry}
              selectedId={selectedEntryId}
              setSelectedId={setSelectedEntryId} />
          ))}
        </div>
      </div>
    </div>
  )
}

export default App
