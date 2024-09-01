
export type Entry = {
    id: number;
    text: string;
    create_time: string;
    actions?: Action[] | string;
    generations?: Generation[] | string;
}

export type Task = {
    id: number;
    text: string;
    start: string | null;
    end: string | null;
    status: string;
    focus?: boolean;
    parent_id?: number | null;
    actions?: Action[];
    parent?: Task | null;
    children?: Task[];
}

export type Action = {
    id: number;
    action: string;
    task_id: number;
    entry_id: number;
    task?: Task;
    entry?: Entry;
}

export type Generation = {
    id: number;
    process: string;
    data: string | object;
    user_comment?: string;
    regenerated?: boolean;
    entry_id: number;
    entry: Entry;
}

