import { useState, useEffect } from "react";
import { GetEntriesHookInterface, EntryQueryInterface } from '../types/components';
import { EntryInterface } from "../types/objects";


const useGetEntries = (): GetEntriesHookInterface => {
    const [entries, setEntries] = useState<EntryInterface[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [trigger, setTrigger] = useState(0);


    useEffect(() => {
        setLoading(true);

        fetch('http://127.0.0.1:2000/entries')
            .then((response) => response.json())
            .then((body: EntryQueryInterface) => {
                setEntries(body.data.entries);
            })
            .catch((error) => {
                setError(error);
            })
            .finally(() => setLoading(false))

    }, [trigger])

    const refetch = () => setTrigger((prev) => prev + 1);

    return { entries, loading, error, refetch }
}


export default useGetEntries;
