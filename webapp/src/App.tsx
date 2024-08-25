import React, { useEffect, useState } from 'react'
import './App.css'

import useGetTasks from './hooks/getTasks';
import { TaskCard } from './components/taskCard';



function App() {
  const { tasks, loading, error, refetch } = useGetTasks();
  const [expandedId, setExpandedId] = useState<number | null>(null);

  if (tasks) console.log({ tasks });
  if (loading) console.log("loading...");
  if (error) console.error("error...");

  useEffect(() => {
    console.log(`task id ${expandedId} selected`)
  }, [expandedId])

  return (
    <div className="column padded">
      <button onClick={refetch} />
      <h1>App will go here</h1>
      {loading && <p>loading</p>}
      {error && <p>{error}</p>}
      <div className="column repeater">
        {tasks && tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            expandedId={expandedId}
            setExpandedId={setExpandedId} />
        ))}
      </div>
    </div>
  )
}

export default App
