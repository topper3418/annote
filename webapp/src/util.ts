
export const formatDate = (dateIn: string | Date | null): string => {
  if (dateIn == null) return 'N/A';
  let inputDate: Date;
  const today = new Date();
  if (typeof (dateIn) === 'string') {
    inputDate = new Date(dateIn);
  }
  else {
    inputDate = dateIn;
  }

  // Check if the date is today
  const isToday = inputDate.toDateString() === today.toDateString();

  if (isToday) {
    // Return time in 12-hour format (e.g., 8:00am)
    const hours = inputDate.getHours();
    const minutes = inputDate.getMinutes();
    const period = hours >= 12 ? 'pm' : 'am';
    const formattedHours = hours % 12 || 12; // Convert 0 or 24 hours to 12
    const formattedMinutes = minutes < 10 ? `0${minutes}` : minutes;

    return `${formattedHours}:${formattedMinutes}${period}`;
  } else {
    // Return date in mm/dd format
    const month = inputDate.getMonth() + 1; // Months are zero-based
    const day = inputDate.getDate();

    return `${month}/${day}`;
  }
}


