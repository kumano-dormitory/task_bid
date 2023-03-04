import * as React from "react";
import { useContext } from "react";
import axios from "../../axios";
import useSWR, { Fetcher } from "swr";
import { ScrollMenu } from "react-horizontal-scrolling-menu";
import { ResponseColumn } from "./ResponseColumn";
import { Date, SlotResponse } from "../../ResponseType";
import { UserContext } from "../../UserContext";
import { isSlot } from "../field/ResponseCard";
import { uniquedays } from "./BidList";
const getCreateSlot: Fetcher<SlotResponse[]> = (url: string) => {
  return axios.get(url).then((response) => response.data);
};

type SlotListProps = {
  url: string;
};

export const SlotList: React.FC<SlotListProps> = (props: SlotListProps) => {
  const { user } = useContext(UserContext);
  const { data, error } = useSWR(
    "/users/" + user.id + props.url,
    getCreateSlot
  );
  if (error) return <div>Loading Failed</div>;
  if (!data) return <div>loading...</div>;
  const days: Date[] | null = isSlot(data[0])
    ? uniquedays(
        Array.from(
          data.map((slot: SlotResponse): Date => {
            return {
              year: slot.start_time.year,
              month: slot.start_time.month,
              day: slot.start_time.day,
            };
          })
        )
      )
    : null;

  return (
    <>
      <ScrollMenu>
        {days ? (
          days.map((day: Date) => {
            return (
              <ResponseColumn
                day={day}
                data={data.filter((slot: SlotResponse) => {
                  return (
                    slot.start_time.year === day.year &&
                    slot.start_time.month === day.month &&
                    slot.start_time.day === day.day
                  );
                })}
              />
            );
          })
        ) : (
          <ResponseColumn day={null} data={data} />
        )}
      </ScrollMenu>
    </>
  );
};
