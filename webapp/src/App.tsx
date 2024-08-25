// import React, { useState, useEffect } from 'react'
import './App.css'
import { TaskCardInterface } from './types/components'
// import { Task } from './types/objects';
import useGetTasks from './hooks/getTasks';


const taskCard: React.FC<TaskCardInterface> = ({ task, expanded }) => {
  const {
    id: taskId,
    text,
    start, end,
    actions,
    children
  } = task;

  return (
    
  )
}

function App() {
  const { tasks, loading, error, refetch } = useGetTasks();

  if (tasks) console.log({ tasks });
  if (loading) console.log("loading...");
  if (error) console.error("error...");

  return (
    <div>
      <button onClick={refetch} />
      <h1>App will go here</h1>
      {loading && <p>loading</p>}
      {error && <p>{error}</p>}
    </div>
  )
}

export default App
