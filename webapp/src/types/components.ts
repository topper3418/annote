import { Entry, Task, Action } from './objects';


export interface BasicFetchHookInterface {
    loading: boolean;
    error: string | null;
    refetch: () => void;
}

export interface GetTasksHookInterface extends BasicFetchHookInterface {
    tasks: Task[];
}

export interface RootQueryInterface {
    data: {
        tasks: Task[];
    }
}

export interface TaskCardInterface {
    task: Task;
    expandedId: number | null;
    setExpandedId: (taskId: number) => void;
}

