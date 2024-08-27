
export type Entry = {
    id: number;
    text: string;
    create_time: Date;
    actions?: Action[];
}

export type Task = {
    id: number;
    text: string;
    start: Date | null;
    end: Date | null;
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
