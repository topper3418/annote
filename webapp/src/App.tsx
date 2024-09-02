import React, { useEffect, useState } from 'react'
import './App.css'

import useGetTasks from './hooks/getTasks';
import useGetEntries from './hooks/getEntries';
import { TaskCard } from './components/taskCard';
import { EntryCard } from './components/entryCard';
import useGetAppData from './hooks/getAppData';
import useSubmitEntry from './hooks/submitNewEntry';
import InputBox from './components/inputBox';



function App() {
  // const { tasks, loading: tasksLoading, error: tasksError, refetch: tasksRefetch } = useGetTasks();
  // const { entries, loading: entriesLoading, error: entriesError, refetch: entriesRefetch } = useGetEntries();
  const {
    tasks,
    entries,
    tasksLoading,
    tasksError,
    entriesLoading,
    entriesError,
    loading,
    error,
  } = useGetAppData();
  const {
    submitEntry,
    loading: submissionProcessing,
    error: submissionError,
    response: submissionResponse
  } = useSubmitEntry();
  const [expandedTaskId, setExpandedTaskId] = useState<number | null>(null);
  const [selectedEntryId, setSelectedEntryId] = useState<number | null | undefined>(null);
  const [newEntryInput, setNewEntryInput] = useState('');

  if (tasksLoading) console.log("loading tasks...");
  if (tasksError) console.error("error loading tasks: ", tasksError);
  if (entriesLoading) console.log("loading entries...");
  if (entriesError) console.error("error loading entries: ", entriesError);
  // if (entries) console.log("entries: ", entries);
  // if (tasks) console.log("tasks: ", tasks);

  useEffect(() => {
    console.log(`task id ${expandedTaskId} selected`)
  }, [expandedTaskId])

  const setSelectedId = (entryId: number | null | undefined) => {
    setSelectedEntryId(entryId)
  }

  return (
    <div className="column padded fill space-between">
      <div className='column'>
        <h1>Annote</h1>
        <div className="row spaced">
          <div className="column repeater width-60 padded">
            <h3>Tasks</h3>
            {tasks && tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                expandedId={expandedTaskId}
                setExpandedId={setExpandedTaskId} />
            ))}
          </div>
          <div className="column repeater width-40 padded">
            <h3>Entries</h3>
            {entries && entries.map((entry) => (
              <EntryCard
                key={entry.id}
                entry={entry}
                selectedId={selectedEntryId}
                setSelectedId={setSelectedId} />
            ))}
          </div>
        </div>
      </div>
      <InputBox
        entry={newEntryInput}
        setNewEntry={setNewEntryInput}
        submitCallback={submitEntry} />
    </div >
  )
}

export default App
