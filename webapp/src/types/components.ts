import { EntryInterface, TaskInterface, ActionInterface, GenerationInterface } from './objects';


export interface BasicFetchHookInterface {
    loading: boolean;
    error: string | null;
    refetch: () => void;
}

export interface GetTasksHookInterface extends BasicFetchHookInterface {
    tasks: TaskInterface[];
}

export interface GetEntriesHookInterface extends BasicFetchHookInterface {
    entries: EntryInterface[];
}

export interface GetAppDataHookInterface extends BasicFetchHookInterface {
    entries: EntryInterface[];
    entriesLoading: boolean;
    entriesError: string | null;
    tasks: TaskInterface[];
    tasksLoading: boolean;
    tasksError: string | null;
}

export interface TaskQueryInterface {
    data: {
        tasks: TaskInterface[];
    }
}

export interface EntryQueryInterface {
    data: {
        entries: EntryInterface[];
    }
}

export interface LatestQueryInterface {
    data: {
        entry: number;
        task: number;
        generation: number;
    }
}

export interface TaskCardInterface {
    task: TaskInterface;
    expandedId?: number | null;
    setExpandedId?: (taskId: number | null) => void;
}

export interface EntryCardInterface {
    entry: EntryInterface;
    selectedId?: number | null;
    setSelectedId?: (entryId: number | null | undefined) => void;
}

export interface InputBoxInterface {
    submitCallback: (newEntry: string) => void;
    entry: string;
    setNewEntry: (newEntry: string) => void;
}

