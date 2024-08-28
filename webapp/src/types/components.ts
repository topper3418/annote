import { Entry, Task, Action } from './objects';


export interface BasicFetchHookInterface {
    loading: boolean;
    error: string | null;
    refetch: () => void;
}

export interface GetTasksHookInterface extends BasicFetchHookInterface {
    tasks: Task[];
}

export interface GetEntriesHookInterface extends BasicFetchHookInterface {
    entries: Entry[];
}

export interface TaskQueryInterface {
    data: {
        tasks: Task[];
    }
}

export interface EntryQueryInterface {
    data: {
        entries: Entry[];
    }
}

export interface TaskCardInterface {
    task: Task;
    expandedId?: number | null;
    setExpandedId?: (taskId: number | null) => void;
}

export interface EntryCardInterface {
    entry: Entry;
    selectedId?: number | null;
    setSelectedId?: (entryId: number | null | undefined) => void;
}

