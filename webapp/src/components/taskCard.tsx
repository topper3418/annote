import React from 'react'
import { TaskCardInterface } from '../types/components'
import { Task, Action } from '../types/objects';
import { formatTime } from '../util';

export const ConciseTaskCard: React.FC<TaskCardInterface> = ({ task, setExpandedId = () => { } }) => {
  const {
    id: taskId,
    text,
    status,
  } = task;

  return (
    <div className="row" onClick={() => setExpandedId(taskId)}>
      <p style={{ width: "80%" }}>{text}</p>
      <p>{status}</p>
    </div>
  )
}


export const TaskCard: React.FC<TaskCardInterface> = ({ task, expandedId, setExpandedId }) => {
  const {
    id: taskId,
    text,
    start, end,
    actions,
    children
  } = task;

  const ConciseChildren = () => {
    return (
      <div className="row">
        <p className="half-width">Children: {children?.length}</p>
        <p className="half-width">Entries: {actions?.length}</p>
      </div>
    )
  }

  const ExpandedChilren = () => {
    return (
      <div className="row">
        <div className="column half-width">
          <p>Children:</p>
          <ul>
            {children && children.map((child: Task) => (
              <li>
                <ConciseTaskCard key={child.id} task={child} />
              </li>
            ))}
          </ul>
        </div>
        <div className="column half-width">
          <p>Entries:</p>
          {actions && actions.map((action: Action) => (
            <p key={action.id}>{action?.entry?.text}</p>
          ))}
        </div>
      </div>
    )
  }

  const onClick = setExpandedId ?
    () => setExpandedId(taskId) :
    () => { };

  return (
    <div className="column card" onClick={onClick}>
      <div className="row">
        <h2 style={{ width: "80%" }}>{text}</h2>
        <div className="column">
          <p>Start: {formatTime(start)}</p>
          <p>End: {formatTime(end)}</p>
        </div>
      </div>
      {expandedId == taskId ?
        <ExpandedChilren /> :
        <ConciseChildren />}
    </div>
  )
}
