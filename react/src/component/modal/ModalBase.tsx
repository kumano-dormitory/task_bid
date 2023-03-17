import React from 'react';
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import Button from "@mui/material/Button";

type ModalProps = {
    title: string;
    open: boolean;
    handleClose: () => void;
    handleSubmit?: () => void;
    children: React.ReactNode;
  };

export const ModalBase: React.FC<ModalProps> = (
    props: ModalProps
  ) => {
    return (
      <Dialog open={props.open} onClose={props.handleClose}>
            <DialogTitle>{props.title}</DialogTitle>
        <DialogContent>
            {props.children}
        </DialogContent>
        <DialogActions>
                <Button onClick={props.handleClose}>Cancel</Button>
        </DialogActions>
      </Dialog>
    );
  };