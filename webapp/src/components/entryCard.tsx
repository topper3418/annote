import React from 'react'
import { EntryCardInterface } from '../types/components'
import { DateCard } from './dateCard';
import { formatDate } from '../util';



export const EntryCard: React.FC<EntryCardInterface> = ({ entry, selectedId, setSelectedId }) => {
  const onClick = setSelectedId ?
    () => setSelectedId(selectedId == entry.id ? undefined : selectedId) :
    () => { };

  return (
    <div className="row card spaced align-top" onClick={onClick}>
      <DateCard date_in={entry.create_time} />
      <p className="fill width-60">{entry.text}</p>
    </div>
  )
} 
