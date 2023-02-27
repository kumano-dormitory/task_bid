import * as React from "react";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import { BidResponse } from "./BidList";
import { Modal,Box } from "@mui/material";

type BidCardProps = {
  bid: BidResponse;
};

const style = {
    position: 'absolute' as 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
  };

export const BidCard: React.FC<BidCardProps> = (props: BidCardProps) => {
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  return (
    <Card
      style={{
        width: "240px",
        display: "inline-block",
      }}
    >
      <CardContent>
        <Typography gutterBottom variant="h6" component="div">
          {props.bid.name}
        </Typography>
        <Typography variant="body2" color="text.secondary" align="right">
          {props.bid.slot.start_time.hour}時{props.bid.slot.start_time.minute}
          分開始 回答締め切り:{props.bid.close_time.month}月
          {props.bid.close_time.day}日
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small">Share</Button>
        <Button size="small" onClick={handleOpen}>
          Open modal
        </Button>
        <Modal
          open={open}
          onClose={handleClose}
          aria-labelledby="modal-modal-title"
          aria-describedby="modal-modal-description"
        >
          <Box sx={style}>
            <Typography id="modal-modal-title" variant="h6" component="h2">
              Text in a modal
            </Typography>
            <Typography id="modal-modal-description" sx={{ mt: 2 }}>
              Duis mollis, est non commodo luctus, nisi erat porttitor ligula.
            </Typography>
          </Box>
        </Modal>
      </CardActions>
    </Card>
  );
};

