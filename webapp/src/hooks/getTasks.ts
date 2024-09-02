import { useState, useEffect } from "react";
import { GetTasksHookInterface, TaskQueryInterface } from '../types/components';
import { TaskInterface } from "../types/objects";


const useGetTasks = (): GetTasksHookInterface => {
    const [tasks, setTasks] = useState<TaskInterface[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [trigger, setTrigger] = useState(0);


    useEffect(() => {
        setLoading(true);

        fetch('http://127.0.0.1:2000/tasks')
            .then((response) => response.json())
            .then((body: TaskQueryInterface) => {
                setTasks(body.data.tasks);
            })
            .catch((error) => {
                setError(error);
            })
            .finally(() => setLoading(false))

    }, [trigger])

    const refetch = () => setTrigger((prev) => prev + 1);

    return { tasks, loading, error, refetch }
}


export default useGetTasks;
