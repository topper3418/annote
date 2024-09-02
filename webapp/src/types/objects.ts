
export type EntryInterface = {
    id: number;
    text: string;
    create_time: string;
    actions?: ActionInterface[] | string;
    generations?: GenerationInterface[] | string;
}

export type TaskInterface = {
    id: number;
    text: string;
    start: string | null;
    end: string | null;
    status: string;
    focus?: boolean;
    parent_id?: number | null;
    actions?: ActionInterface[];
    parent?: TaskInterface | null;
    children?: TaskInterface[];
}

export type ActionInterface = {
    id: number;
    action: string;
    task_id: number;
    entry_id: number;
    task?: TaskInterface;
    entry?: EntryInterface;
}

export type GenerationInterface = {
    id: number;
    process: string;
    data: string | object;
    user_comment?: string;
    regenerated?: boolean;
    entry_id: number;
    entry: EntryInterface;
}

