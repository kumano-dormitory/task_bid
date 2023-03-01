import * as React from "react";
import { useContext } from "react";
import axios from "./axios";
import useSWR, { Fetcher } from "swr";
import SlotCard from "./SlotCard";
import {  List, ListSubheader } from "@mui/material";
import { ScrollMenu } from "react-horizontal-scrolling-menu";
import { ResponseColumn } from "./ResponseColumn";
import { Date, SlotResponse } from "./ResponseType";
import { UserContext } from "./UserContext";
const getCreateSlot: Fetcher<SlotResponse[]> = (url: string) => {
  return axios.get(url).then((response) => response.data);
};

type CreateListProps = {
  url:string,
}

export const CreateList: React.FC<CreateListProps> = (props:CreateListProps) => {
  const { user } = useContext(UserContext);
  const { data, error } = useSWR(
    "/users/" + user.id + props.url,
    getCreateSlot
  );
  if (error) return <TestList />;
  if (!data) return <div>loading...</div>;
  const days: Date[] = Array.from(
    new Set(
      data.map((slot: SlotResponse): Date => {
        return {
          year: slot.start_time.year,
          month: slot.start_time.month,
          day: slot.start_time.day,
        };
      })
    )
  );

  return (
    <>
      <ScrollMenu>
        {days.map((day: Date) => {
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
        })}
      </ScrollMenu>
    </>
  );
};

const TestList: React.FC = () => {
  return (
    <>
      <ScrollMenu>
        <List
          sx={{
            width: "100%",
            maxWidth: 360,
            bgcolor: "background.paper",
            position: "relative",
            overflow: "auto",
            maxHeight: 680,
            "& ul": { padding: 0 },
          }}
          subheader={<li />}
        >
          <SlotCard />
          <SlotCard />
          <SlotCard />
        </List>
        <List
          sx={{
            width: "100%",
            maxWidth: 360,
            bgcolor: "background.paper",
            position: "relative",
            overflow: "auto",
            maxHeight: 680,
            "& ul": { padding: 0 },
          }}
          subheader={<li />}
        >
          <ListSubheader>ajfa</ListSubheader>
          <SlotCard />
          <SlotCard />
          <SlotCard />
          <SlotCard />
          <SlotCard />
          <SlotCard />
          <SlotCard />
          <SlotCard />
          <SlotCard />
        </List>
        <List
          sx={{
            width: "100%",
            maxWidth: 360,
            bgcolor: "background.paper",
            position: "relative",
            overflow: "auto",
            maxHeight: 680,
            "& ul": { padding: 0 },
          }}
          subheader={<li />}
        >
          <SlotCard />
          <SlotCard />
          <SlotCard />
        </List>
      </ScrollMenu>
    </>
  );
};
