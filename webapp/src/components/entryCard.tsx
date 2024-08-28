import React from 'react'
import { EntryCardInterface } from '../types/components'
import { Task, Action } from '../types/objects';
import { formatTime } from '../util';



export const EntryCard: React.FC<EntryCardInterface> = ({ entry, selectedId, setSelectedId }) => {
  const onClick = setSelectedId ?
    () => setSelectedId(selectedId == entry.id ? null : selectedId) :
    () => { };

  return (
    <div className="row" onClick={onClick}>
      <p>{entry.create_time}</p>
      <p>{entry.text}</p>
    </div>
  )
} 
