import { InputBoxInterface } from "../types/components";

const InputBox: React.FC<InputBoxInterface> = ({ entry, setNewEntry, submitCallback }) => {

  const submitAndClear = () => {
    submitCallback(entry);
    setNewEntry('');
  }

  const listenKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) submitAndClear();
  }


  return (
    <div className='row centered spaced'>
      <textarea
        value={entry}
        onKeyDown={listenKeyDown}
        onChange={(event) => setNewEntry(event.target.value)}
        placeholder='new entry...'
        style={{
          width: "500px",
          height: "200px",
          padding: "10px"
        }} />
      <button onClick={submitAndClear}>
        submit
      </button>
    </div>
  )
}


export default InputBox;
