import * as React from "react";
import DialogContentText from "@mui/material/DialogContentText";
import { ModalBase } from "./ModalBase";
import { Button } from "@mui/material";
type ModalProps = {
  open: boolean;
  names: string[];
  text: string;
  handleClose: () => void;
  handleSubmit: () => void;
};

export const ConfirmModal: React.FC<ModalProps> = (props: ModalProps) => {
  return (
    <ModalBase
      title={"確認画面"}
      open={props.open}
      handleClose={props.handleClose}
    >
      <DialogContentText>
        {props.text}
        {props.names.map((name) => {
          return <li>{name}</li>;
        })}
      </DialogContentText>
      <Button onClick={props.handleSubmit}>削除する</Button>
    </ModalBase>
  );
};
