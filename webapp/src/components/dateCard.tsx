import React from 'react'
import { formatDate } from '../util';


interface DateCardInterface {
  date_in: string | Date | null;
}

export const DateCard: React.FC<DateCardInterface> = ({ date_in }) => {

  return (
    <div className="small-card column square-40 centered">
      <p>{formatDate(date_in)}</p>
    </div>
  )
} 
