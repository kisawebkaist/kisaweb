import {
    RawDraftContentState,
} from "draft-js";

export type EventT = {
    title: string;
    slug: string;
    start_datetime: string;
    end_datetime: string;
    reg_start_datetime: string;
    reg_end_datetime: string;
    max_occupancy: number;
    current_occupancy: number;
    important_message: string;
    tags: TagT[];

    description: RawDraftContentState;
};

export type EventT_Partial = Omit<EventT, "description">;
export type TagT = {tag_name: string };