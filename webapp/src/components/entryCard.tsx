import React from 'react'
import { EntryCardInterface } from '../types/components'
import { formatTime } from '../util';



export const EntryCard: React.FC<EntryCardInterface> = ({ entry, selectedId, setSelectedId }) => {
  const onClick = setSelectedId ?
    () => setSelectedId(selectedId == entry.id ? undefined : selectedId) :
    () => { };

  const dateCardStyle: React.CSSProperties = {
    width: "50px",
    height: "50px",
    textAlign: "center",
  }

  return (
    <div className="row card spaced align-top" onClick={onClick}>
      <div className="small-card column centered">
        <p style={dateCardStyle}>{formatTime(entry.create_time)}</p>
      </div>
      <p className="fill width-60">{entry.text}</p>
    </div>
  )
} 
