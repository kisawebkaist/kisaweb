import axios from "axios";
import {
    RawDraftContentState,
} from "draft-js";

export type EventT_Complete = {
    title: string;
    slug: string;
    event_start_datetime: string;
    event_end_datetime: string;
    reg_start_datetime: string;
    reg_end_datetime: string;
    max_occupancy: number;
    current_occupancy: number;
    important_message: string;
    poster: string;

    description: RawDraftContentState;
};

export type EventT_Partial = Omit<EventT_Complete, "description">;
export type TagT = { tag_name: string };

export class EventAPI {
    static async allEvents(queryParams: Record<string, any>): Promise<EventT_Partial[]> {
        const resp = await axios.get(`${process.env.REACT_APP_API_ENDPOINT}/event/`, queryParams);
        return resp.data;
    }
    static async getEvent(slug: string): Promise<EventT_Complete> {
        const resp = await axios.get(`${process.env.REACT_APP_API_ENDPOINT}/event/${slug}`);
        return resp.data;
    }
}