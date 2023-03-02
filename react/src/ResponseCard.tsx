import * as React from "react";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import {
  ResponseBase,
  BidResponse,
  SlotResponse,
  TaskResponse,
} from "./ResponseType";
import { Modal, Box } from "@mui/material";

type ResponseCardProps<T extends ResponseBase> = {
  data: T;
};

type ResponseDisplayProps = {
  data: BidResponse | SlotResponse | TaskResponse;
};

const style = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

export const ResponseCard: React.FC<
  ResponseCardProps<BidResponse | SlotResponse | TaskResponse>
> = (props: ResponseCardProps<BidResponse | SlotResponse | TaskResponse>) => {
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
          {props.data.name}
        </Typography>
        <ResponseDisplay data={props.data} />
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

export const ResponseDisplay: React.FC<ResponseDisplayProps> = (
  props: ResponseDisplayProps
) => {
  if (isBid(props.data)) {
    return (
      <Typography variant="body2" color="text.secondary" align="right">
        {props.data.slot.start_time.hour}時{props.data.slot.start_time.minute}
        分開始 回答締め切り:{props.data.close_time.month}月
        {props.data.close_time.day}日
      </Typography>
    );
  } else if (isSlot(props.data)) {
    return (
      <Typography variant="body2" color="text.secondary" align="right">
        {props.data.start_time.hour}時{props.data.start_time.minute}分開始
        {props.data.end_time.hour}時{props.data.end_time.minute}分終了
      </Typography>
    );
  } else if (isTask(props.data)) {
    return (
      <Typography variant="body2" color="text.secondary" align="right">
        最低限必要な人数:{props.data.min_worker_num}人 その中で必要な経験者の数:
        {props.data.exp_worker_num}人 最大人数:{props.data.max_worker_num}人
      </Typography>
    );
  } else {
    return (
      <Typography variant="body2" color="text.secondary" align="right">
        表示できる情報はありません
      </Typography>
    );
  }
};

const isBid = (data: any): data is BidResponse => {
  return !!(data as BidResponse)?.buyout_point;
};

export const isSlot = (data: any): data is SlotResponse => {
  return !!(data as SlotResponse)?.start_time;
};

export const isTask = (data: any): data is TaskResponse => {
  return !!(data as TaskResponse)?.exp_worker_num;
};
