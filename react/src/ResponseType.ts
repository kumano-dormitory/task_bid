import { Fetcher } from "swr";
import axios from "./axios";
export type ResponseBase = {
    id: string;
    name: string;
  };
  export type Date = {
    year: number;
    month: number;
    day: number;
  };
  
  type CreaterResponse = ResponseBase & {
    block: "A1" | "A2" | "A3" | "A4" | "B12" | "B3" | "B4" | "C12" | "C34";
    room_number: string;
  };
  
  type Datetime = {
    year: number;
    month: number;
    day: number;
    hour: number;
    minute: number;
  };
  
  type BidSlot = ResponseBase & {
    start_time: Datetime;
    end_time: Datetime;
  };
  
  export type TaskResponse = ResponseBase & {
    detail: string;
    max_woker_num: number;
    min_woker_num: number;
    exp_woker_num: number;
    creater_id: string;
    creater: string;
  };
  
  export type BidResponse = ResponseBase & {
    open_time: Datetime;
    close_time: Datetime;
    slot: BidSlot;
    start_point: number;
    buyout_point: number;
    is_complete: boolean;
  };
  
  export type SlotResponse = ResponseBase & {
    start_time: Datetime;
    end_time: Datetime;
    creater: CreaterResponse;
    task: TaskResponse;
  };

export type TaskTagsResponse = {
  id: string;
  name: string;
};

export type AuthorityResponse = {
  id: string;
  name: string;
  url: string;
  method: "GET" | 'POST' | "PATCH" | "PUT" | "DELETE";
}

export const getData =(url: string) => {
  return axios.get(url).then((response)=>response.data)
}