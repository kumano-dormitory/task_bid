import * as React from "react";
import Button from "@mui/material/Button";
import DialogContentText from "@mui/material/DialogContentText";
import { SlotResponse } from "../../ResponseType";
import { Typography } from "@mui/material";
import { ModalBase } from "./ModalBase";
type ModalProps = {
  open: boolean;
  slot: SlotResponse;
  handleClose: () => void;
  handleDelete: () => void;
};

type SlotInfoTextProps = {
  slot: SlotResponse;
  handleDelete: () => void;
};

export const SlotInfo: React.FC<ModalProps> = (props: ModalProps) => {
  return (
    <ModalBase title="詳細" open={props.open} handleClose={props.handleClose}>
      <DialogContentText>
        <SlotInfoText slot={props.slot} handleDelete={props.handleDelete} />
      </DialogContentText>
    </ModalBase>
  );
};

const SlotInfoText: React.FC<SlotInfoTextProps> = (
  props: SlotInfoTextProps
) => {
  return (
    <>
      <Typography component={"h5"} variant="h5">
        {props.slot.name}
      </Typography>
      <Typography variant="body1">
        <li>
          開始時刻:{props.slot.start_time.year}年{props.slot.start_time.month}月
          {props.slot.start_time.day}日{props.slot.start_time.hour}時
          {props.slot.start_time.minute}分
        </li>
        <li>
          終了時刻:{props.slot.end_time.year}年{props.slot.end_time.month}月
          {props.slot.end_time.day}日{props.slot.end_time.hour}時
          {props.slot.end_time.minute}分
        </li>
        <li>作成者:{props.slot.creater.name}</li>
        <li>タスク:{props.slot.task.name}</li>
      </Typography>
      <Button onClick={props.handleDelete} >テンプレートから外す</Button>
    </>
  );
};
