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
} from "../../ResponseType";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import { SingleChoiceField } from "./SIngleChoiceField";
import { DateSelect } from "./DateSelect";
import { Modal, Box } from "@mui/material";
import { SlotForm } from "../form/SlotForm";
import dayjs, { Dayjs } from "dayjs";
import { SimpleChoiceField } from "./SimpleChoiceField";
import { TabContext } from "../RecruitPage";
type ResponseCardProps<T extends ResponseBase> = {
  data: T;
};

type ResponseDisplayProps = {
  data: BidResponse | SlotResponse | TaskResponse;
};

type ResponseModalProps = {
  open: boolean;
  handleClose: () => void;
  handleSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
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
        <ResponseModalBase
          open={open}
          handleClose={handleClose}
          handleSubmit={(event) => {}}
          data={props.data}
        />
      </CardActions>
    </Card>
  );
};

const ResponseModalBase: React.FC<ResponseModalProps> = (
  props: ResponseModalProps
) => {
  const value=React.useContext(TabContext)
  return (
    <Dialog open={props.open} onClose={props.handleClose}>
      <DialogTitle>Subscribe</DialogTitle>
      <DialogContent>
        <DialogContentText>
          To subscribe to this website, please enter your email address here. We
          will send updates occasionally.
        </DialogContentText>
        <Box
          component="form"
          noValidate
          onSubmit={props.handleSubmit}
          sx={{ mt: 3 }}
        >
          { value===0 ? (
            <TenderModalField data={props.data} />
          ) : isSlot(props.data) ? (
            <SlotModalField data={props.data} />
          ) : (
            <></>
          )}

          <Button type="submit">Subscribe</Button>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={props.handleClose}>Cancel</Button>
      </DialogActions>
    </Dialog>
  );
};

const AssignModalField: React.FC = () => {
  return()
}



const TenderModalField: React.FC<ResponseCardProps<BidResponse>> = (
  props: ResponseCardProps<BidResponse>
) => {
  return (
    <Grid item xs={12}>
      <TextField
        id="tender_point"
        name="tender_point"
        inputProps={{ min: String(props.data.buyout_point), step: "1" }}
        label="入札ポイント"
        defaultValue={String(props.data.start_point)}
        type="number"
      />
    </Grid>
  );
};

const LackModalField: React.FC = () => {
  return()
}

const LackExpModalField: React.FC = () => {
  return()
}

const EndSlotModalField: React.FC = () => {
  return()
}




const SlotModalField: React.FC<ResponseCardProps<SlotResponse>> = (
  props: ResponseCardProps<SlotResponse>
) => {
  const [starttime, setStarttime] = React.useState<Dayjs | null>(dayjs());
  const [endtime, setEndtime] = React.useState<Dayjs | null>(dayjs());
  const [id, setID] = React.useState<string>("None");
  return (
    <Grid container spacing={2}>
      <Grid item xs={12} sm={6}>
        <TextField
          autoComplete="given-name"
          name="name"
          required
          fullWidth
          id="name"
          label="名前"
          autoFocus
        />
      </Grid>
      <Grid item xs={12} sm={6}>
        <DateSelect
          title="集合時刻"
          date={starttime}
          setValue={setStarttime}
          setOther={{ setOther: setEndtime, timedelta: 1, unit: "h" }}
        />
      </Grid>
      <Grid item xs={12}>
        <DateSelect title="終了予定時刻" date={endtime} setValue={setEndtime} />
      </Grid>
      <Grid>
        <SingleChoiceField
          url="/tasks/"
          title="タスク"
          id={id}
          setData={setID}
        />
      </Grid>
    </Grid>
  );
};

const 

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
