import axios from "./axios";
import { Fetcher } from "swr";
export type ListProps = {
  url: string;
};
export type ResponseBase = {
  id: string;
  name: string;
};
export type Date = {
  year: number;
  month: number;
  day: number;
};

export type UserResponse = ResponseBase & {
  block: string;
  room_number: string;
  exp_task: TaskResponse[];
  slots: ResponseBase[];
  create_slot: ResponseBase[];
  create_task: ResponseBase[];
  point: number;
  bid: ResponseBase[];
  is_active: boolean;
};

type CreaterResponse = ResponseBase & {
  block: "A1" | "A2" | "A3" | "A4" | "B12" | "B3" | "B4" | "C12" | "C34";
  room_number: string;
};

export type Datetime = {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
};

export const datetimeParse = (datetime: Datetime): string => {
  return `${datetime.year}年${datetime.month}月${datetime.day}日${datetime.hour}時${datetime.minute}分`;
};
export const noYeardatetimeParse = (datetime: Datetime): string => {
  return `${datetime.month}月${datetime.day}日${datetime.hour}時${datetime.minute}分`;
};

type BidSlot = ResponseBase & {
  start_time: Datetime;
  end_time: Datetime;
  assignees: ResponseBase[];
};

export type TaskResponse = ResponseBase & {
  detail: string;
  max_worker_num: number;
  min_worker_num: number;
  exp_worker_num: number;
  start_point: number;
  buyout_point: number;
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
  user_bidpoint: number | "notyet";
};

export type BidderResponse = ResponseBase & {
  user_id: string;
  user: string;
  point: number;
  is_canceled: boolean;
};

export type SlotResponse = ResponseBase & {
  start_time: Datetime;
  end_time: Datetime;
  assignees: ResponseBase[];
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
  method: "GET" | "POST" | "PATCH" | "PUT" | "DELETE";
};

export type TemplateResponse = {
  id: string;
  name: string;
  slots: SlotResponse[];
};
export const getData = (url: string) => {
  return axios.get(url).then((response) => response.data);
};
