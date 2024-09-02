import React, { useState, useEffect, useRef } from "react";
import { GetAppDataHookInterface, EntryQueryInterface, LatestQueryInterface } from '../types/components';
import { EntryInterface, GenerationInterface, TaskInterface } from "../types/objects";
import useGetEntries from "./getEntries";
import useGetTasks from "./getTasks";

interface LatestInterface {
    task?: number;
    entry?: number;
    generation?: number;
}

const useGetAppData = (): GetAppDataHookInterface => {
    const {
        entries,
        loading: entriesLoading,
        error: entriesError,
        refetch: entriesRefetch
    } = useGetEntries();
    const {
        tasks,
        loading: tasksLoading,
        error: tasksError,
        refetch: tasksRefetch
    } = useGetTasks();
    // const [latest, _setLatest] = useState<LatestInterface>({});
    const latest = useRef<LatestInterface>({});
    const [loading, setLatestLoading] = useState(false);
    const [error, setLatestError] = useState(null);

    const setLatest = (newLatest: LatestInterface) => {
        const oldLatest = latest.current;
        if (oldLatest.task != newLatest.task) tasksRefetch()
        else if (oldLatest.entry != newLatest.entry) entriesRefetch()
        else if (oldLatest.generation != newLatest.generation) {
            entriesRefetch()
            tasksRefetch()
        }
        latest.current = newLatest;
    }


    const refetch = () => {
        setLatestLoading(true);

        fetch('http://127.0.0.1:2000/latest')
            .then((response) => {
                if (!response.ok) {
                    console.error('response.status')
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then((body: LatestQueryInterface) => {
                setLatest(body.data)
            })
            .catch((error) => {
                setLatestError(error);
            })
            .finally(() => setLatestLoading(false))
    }

    useEffect(() => {
        refetch()
        const intervalId = setInterval(refetch, 1000);
        return () => clearInterval(intervalId);
    }, [])

    return {
        tasks,
        entries,
        tasksLoading,
        tasksError,
        entriesLoading,
        entriesError,
        loading,
        error,
        refetch: () => { console.log('refetch not implemented on getAppData') }
    }

}


export default useGetAppData;
