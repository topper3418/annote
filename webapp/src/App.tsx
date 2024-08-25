import React, { useEffect, useState } from 'react'
import './App.css'
import { TaskCardInterface } from './types/components'
// import { Task } from './types/objects';
import useGetTasks from './hooks/getTasks';


const TaskCard: React.FC<TaskCardInterface> = ({ task, expandedId, setExpandedId }) => {
  const {
    id: taskId,
    text,
    start, end,
    actions,
    children
  } = task;

  return (
    <div className="column card" onClick={() => setExpandedId(taskId)}>
      <div className="row">
        <h2 style={{ width: "60%" }}>{text}</h2>
        <div className="column">
          <p>Start: {String(start)}</p>
          <p>End: {String(end)}</p>
        </div>
      </div>
      <div className="row">
        <p className="half-width">Children: {children?.length}</p>
        <p className="half-width">Entries: {actions?.length}</p>
      </div>
    </div>
  )
}

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
            task={task}
            expandedId={expandedId}
            setExpandedId={setExpandedId} />
        ))}
      </div>
    </div>
  )
}

export default App
