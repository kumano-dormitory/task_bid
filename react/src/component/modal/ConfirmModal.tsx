import * as React from "react";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";


type ModalProps = {
    open: boolean;
  names: string[];
  text: string;
    handleClose: () => void;
    handleSubmit: () => void;
}

export const ConfirmModal: React.FC<ModalProps> = (
    props: ModalProps
) => {
    return (
      <Dialog open={props.open} onClose={props.handleClose}>
        <DialogTitle>確認画面</DialogTitle>
        <DialogContent>
                <DialogContentText>
                    {props.text}
                    {props.names.map((name) => {
                        return <li>{name}</li>
            })}
          </DialogContentText>
          
        </DialogContent>
        <DialogActions>
                <Button onClick={props.handleClose}>Cancel</Button>
                <Button onClick={props.handleSubmit}>Subscribe</Button>
        </DialogActions>
      </Dialog>
    );
  };
  