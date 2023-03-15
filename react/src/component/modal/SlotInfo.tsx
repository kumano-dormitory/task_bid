import * as React from "react";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import { SlotResponse } from "../../ResponseType";
import { Typography } from "@mui/material";

type ModalProps = {
  open: boolean;
  slot: SlotResponse;
  handleClose: () => void;
  handleDelete: () => void;
};

type SlotInfoTextProps = {
  slot: SlotResponse;
};

export const SlotInfo: React.FC<ModalProps> = (props: ModalProps) => {
  return (
    <Dialog open={props.open} onClose={props.handleClose}>
      <DialogTitle>詳細</DialogTitle>
      <DialogContent>
        <DialogContentText><SlotInfoText slot={props.slot}/></DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={props.handleClose}>Cancel</Button>
        <Button onClick={props.handleDelete}>テンプレートから外す</Button>
      </DialogActions>
    </Dialog>
  );
};

const SlotInfoText: React.FC<SlotInfoTextProps> = (
  props: SlotInfoTextProps
) => {
  return (
    <>
      <Typography component={"h3"} variant="h3">
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
    </>
  );
};
