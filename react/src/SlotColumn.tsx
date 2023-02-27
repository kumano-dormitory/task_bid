import React from "react";
import { Date } from "./BidList";
import { BidResponse } from "./BidList";
import { List, ListSubheader } from "@mui/material";
import { BidCard } from "./BidCard";
type SlotColumnProps = {
  day: Date;
  bids: BidResponse[];
};

export const SlotColumn: React.FC<SlotColumnProps> = (
  props: SlotColumnProps
) => {
  return (
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
      <ListSubheader>
        {props.day.month}月{props.day.day}日　{props.bids.length}枠
          </ListSubheader>
          {props.bids.map((bid: BidResponse) => (<BidCard bid={bid} />))}
    </List>
  );
};
