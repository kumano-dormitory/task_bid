import * as React from "react";
import axios from "../../axios";
import useSWR, { Fetcher } from "swr";
import { ScrollMenu } from "react-horizontal-scrolling-menu";
import { ResponseColumn } from "./ResponseColumn";
import { Date, BidResponse } from "../../ResponseType";


export const uniquedays=(days:any[])=>days.filter((value, index) => {
  const _value = JSON.stringify(value);
  return index === days.findIndex(day => {
    return JSON.stringify(day) === _value;
  });
});

type BidListProps = {
  url: string;
};

const getBids: Fetcher<BidResponse[]> = (url: string) => {
  return axios.get(url).then((response) => response.data);
};

export const BidList: React.FC<BidListProps> = (props: BidListProps) => {
  const { data, error } = useSWR(props.url, getBids);
  if (error) return <div>Loading Failed</div>;
  if (!data) return <div>loading...</div>;
  const days: Date[] = Array.from(
    data.map((bid: BidResponse): Date => {
      return {
        year: bid.slot.start_time.year,
        month: bid.slot.start_time.month,
        day: bid.slot.start_time.day,
      };
    })
  );

  

  return (
    <>
      <ScrollMenu>
        {uniquedays(days).map((day: Date) => {
          return (
            <ResponseColumn
              day={day}
              data={data.filter((bid: BidResponse) => {
                return (
                  bid.slot.start_time.year === day.year &&
                  bid.slot.start_time.month === day.month &&
                  bid.slot.start_time.day === day.day
                );
              })}
            />
          );
        })}
      </ScrollMenu>
    </>
  );
};

