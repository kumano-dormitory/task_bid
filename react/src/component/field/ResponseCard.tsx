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
  BidderResponse,
  datetimeParse,
  noYeardatetimeParse,
} from "../../ResponseType";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import { Box } from "@mui/material";
import { TabContext } from "../RecruitPage";
import axios from "../../axios";
import { useSnackbar } from "../Snackbar";
import { ModalBase } from "../modal/ModalBase";
import { useSWRConfig} from "swr";
export type ResponseCardProps<T extends ResponseBase> = {
  data: T;
};

type LackBidDetailProps = {
  data: BidResponse;
  onSubmit:(event: React.FormEvent<HTMLFormElement>) => void
}

type ResponseListDisplayProps = {
  data: BidResponse | SlotResponse | TaskResponse | BidderResponse;
};

type BidderModalProps = {
  data: BidderResponse;
};

export const ResponseCard: React.FC<
  ResponseCardProps<BidResponse | SlotResponse | TaskResponse | BidderResponse>
> = (
  props: ResponseCardProps<
    BidResponse | SlotResponse | TaskResponse | BidderResponse
  >
) => {
  const value = React.useContext(TabContext);
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
        <ResponseListDisplay data={props.data} />
      </CardContent>
      <CardActions>
        <Button size="small" onClick={handleOpen}>
          Open modal
        </Button>
        <ModalBase title={"詳細"} open={open} handleClose={handleClose}>
          {value === 0 && isSlot(props.data) ? (
            <AssignModalField data={props.data} />
          ) : value === 1 && isBid(props.data) ? (
            <TenderModalField data={props.data} />
          ) : value === 2 && isBidder(props.data) ? (
            <ConvertModalField data={props.data} />
          ) : value === 3 && isBid(props.data) ? (
            <LackModalField data={props.data} />
          ) : value === 4 && isBid(props.data) ? (
            <LackExpModalField data={props.data} />
          ) : value === 5 && isSlot(props.data) ? (
            <CheckWorkModalField data={props.data} />
          ) : (
            <div>Failed to load data</div>
          )}
        </ModalBase>
      </CardActions>
    </Card>
  );
};


const AssignModalField: React.FC<ResponseCardProps<SlotResponse>> = (
  props: ResponseCardProps<SlotResponse>
) => {
  const { showSnackbar } = useSnackbar();
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .post(`/slots/${props.data.id}/cancel`, {
        premire_point: data.get("premire_point"),
      })
      .then((response) => {
        showSnackbar("更新成功", "success");
        console.log(response);
      })
      .catch((err) => {
        showSnackbar("更新失敗", "error");
        console.log(err);
      });
  };
  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Typography variant="h6">{props.data.name}</Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="body1">
            {datetimeParse(props.data.start_time)}開始
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="body1">
            {datetimeParse(props.data.end_time)}終了
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="body1">
            仕事内容:{props.data.task.detail}
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Typography variant="body1">
            参加者:
            {props.data.assignees.map((user) => (
              <> {user.name}</>
            ))}
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <TextField
            id="premire_point"
            name="premire_point"
            inputProps={{ min: "0", step: "1" }}
            label="加算ポイント"
            defaultValue="0"
            type="number"
          />
        </Grid>
      </Grid>
      <Button type="submit">交代を申請する</Button>
    </Box>
  );
};


const TenderModalField: React.FC<ResponseCardProps<BidResponse>> = (
  props: ResponseCardProps<BidResponse>
) => {
  const { showSnackbar } = useSnackbar();
  const { mutate } = useSWRConfig();
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    if (props.data.user_bidpoint === "notyet") {
      axios
        .post(`/bids/${props.data.id}/tender`, {
          tender_point: data.get("tender_point"),
        })
        .then((response) => {
          showSnackbar("更新成功", "success");
          mutate("/bids/");
          console.log(response);
          console.log(props.data.user_bidpoint);
        })
        .catch((err) => {
          showSnackbar("更新失敗", "error");
          console.log(err);
        });
    } else {
      axios
        .patch(`/bids/${props.data.id}`, {
          tender_point: data.get("tender_point"),
        })
        .then((response) => {
          console.log(response);
          mutate("/bids/");
        })
        .catch((err) => {
          console.log(err);
        });
    }
  };
  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
        {props.data.name}
      </Grid>
      <Grid item xs={12}>
        勤務時間:{noYeardatetimeParse(props.data.slot.start_time)}~
        {noYeardatetimeParse(props.data.slot.end_time)}
      </Grid>
      <Grid item xs={12}>
        応募締切{datetimeParse(props.data.close_time)}まで
      </Grid>
      <Grid item xs={12}>
        貰えるポイント:{props.data.buyout_point}~{props.data.start_point}
      </Grid>
      {props.data.user_bidpoint === "notyet" ? (
        <></>
      ) : (
        <Grid item xs={12}>
          {props.data.user_bidpoint}ポイントで応募中
        </Grid>
      )}
        <Grid item xs={12}>
          <TextField
            id="tender_point"
            name="tender_point"
            inputProps={{
              min: String(props.data.buyout_point),
              max: String(props.data.start_point),
              step: "1",
            }}
            label="入札ポイント"
            defaultValue={String(props.data.start_point)}
            type="number"
          />
        </Grid>
      </Grid>
      <Button type="submit">入札する</Button>
    </Box>
  );
};
const LackBidDetail: React.FC<LackBidDetailProps> = (
  props: LackBidDetailProps
) => {
  return (
    <Box component="form" noValidate onSubmit={props.onSubmit} sx={{ mt: 3 }}>
        <Grid container spacing={2}>
      <Grid item xs={12}>
        {props.data.name}
      </Grid>
      <Grid item xs={12}>
        勤務時間:{noYeardatetimeParse(props.data.slot.start_time)}~
        {noYeardatetimeParse(props.data.slot.end_time)}
      </Grid>
      <Grid item xs={12}>
        貰えるポイント:{props.data.buyout_point - 1}
      </Grid>
      <Grid item xs={12}>
        参加者:
        {props.data.slot.assignees.map((user) => (
          <> {user.name}</>
        ))}
      </Grid>
      {props.data.user_bidpoint === "notyet" ? (
        <Button type="submit">参加する</Button>
      ) : (
        <Grid item xs={12}>
          {props.data.user_bidpoint} ポイントで応募中
        </Grid>
      )}
    </Grid>
    </Box>
  );
};
const LackModalField: React.FC<ResponseCardProps<BidResponse>> = (
  props: ResponseCardProps<BidResponse>
) => {
  const { showSnackbar } = useSnackbar();
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    axios
      .post(`/bids/${props.data.id}/tenderlack`)
      .then((response) => {
        showSnackbar("更新成功", "success");
        console.log(response);
      })
      .catch((err) => {
        showSnackbar("更新失敗", "error");
        console.log(err);
      });
  };
  return (
    <LackBidDetail data={props.data} onSubmit={handleSubmit}/>
  );
};

const LackExpModalField: React.FC<ResponseCardProps<BidResponse>> = (
  props: ResponseCardProps<BidResponse>
) => {
  const { showSnackbar } = useSnackbar();
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    axios
      .post(`/bids/${props.data.id}/tenderlack`)
      .then((response) => {
        showSnackbar("更新成功", "success");
        console.log(response);
      })
      .catch((err) => {
        showSnackbar("更新失敗", "error");
        console.log(err);
      });
  };
  return (
    <LackBidDetail data={props.data} onSubmit={handleSubmit}/>
  );
};

const ConvertModalField: React.FC<BidderModalProps> = (
  props: BidderModalProps
) => {
  const { showSnackbar } = useSnackbar();
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    axios
      .patch(`/bids/${props.data.id}/convert`, {
        user_id: props.data.user_id,
      })
      .then((response) => {
        showSnackbar("更新成功", "success");
        console.log(response);
      })
      .catch((err) => {
        showSnackbar("更新失敗", "error");
        console.log(err);
      });
  };

  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          仕事:{props.data.name}
        </Grid>
        <Grid item xs={12}>
          貰えるポイント:{props.data.point}
        </Grid>
      </Grid>
      <Button type="submit">交代する</Button>
    </Box>
  );
};

const CheckWorkModalField: React.FC<ResponseCardProps<SlotResponse>> = (
  props: ResponseCardProps<SlotResponse>
) => {
  const { showSnackbar } = useSnackbar();
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    axios
      .post(`/slots/${props.data.id}/complete`)
      .then((response) => {
        showSnackbar("更新成功", "success");
        console.log(response);
      })
      .catch((err) => {
        showSnackbar("更新失敗", "error");
        console.log(err);
      });
  };

  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Grid container spacing={2}>
        <Grid item xs={12}>仕事:{props.data.name}</Grid>
      </Grid>
      <Button type="submit">仕事をしました</Button>
    </Box>
  );
};

export const ResponseListDisplay: React.FC<ResponseListDisplayProps> = (
  props: ResponseListDisplayProps
) => {
  const value = React.useContext(TabContext);
  if (value === 0 && isSlot(props.data)) {
    return (
      <Typography variant="body2" color="text.secondary" align="left">
        <p>
          {props.data.start_time.hour}時{props.data.start_time.minute}分開始
        </p>
        <p>
          {props.data.end_time.hour}時{props.data.end_time.minute}分終了
        </p>
      </Typography>
    );
  } else if (value === 1 && isBid(props.data)) {
    return (
      <>
        <Typography variant="body2" color="text.secondary" align="right">
          <p>
            {props.data.slot.start_time.hour}時
            {props.data.slot.start_time.minute}
            分開始
          </p>{" "}
          <p>
            回答締め切り:{props.data.close_time.month}月
            {props.data.close_time.day}日
          </p>
        </Typography>
        {props.data.user_bidpoint !== "notyet" ? (
          <Typography variant="body2" color="success" align="center">
            入札済み:{props.data.user_bidpoint}
          </Typography>
        ) : (
          <></>
        )}
      </>
    );
  } else if (value === 2 && isBidder(props.data)) {
    return (
      <Typography variant="body2" color="text.secondary" align="right">
        <p>交代申請者{props.data.user}</p>
        <p>交代したい仕事{props.data.name}</p>
        <p>交代して貰えるポイント{props.data.point}</p>
      </Typography>
    );
  } else if ((value === 3 || value === 4) && isBid(props.data)) {
    return (
      <Typography variant="body2" color="text.secondary" align="right">
        <p>
          {props.data.slot.start_time.hour}時{props.data.slot.start_time.minute}
          分開始
        </p>
        <p>
          {props.data.slot.end_time.hour}時{props.data.slot.end_time.minute}
          分終了
        </p>
        <p>貰えるポイント：{props.data.buyout_point - 1}</p>
      </Typography>
    );
  } else if (value === 5 && isSlot(props.data)) {
    return (
      <Typography variant="body2" color="text.secondary" align="right">
        <p>貰えるポイント：{props.data.name}</p>
      </Typography>
    );
  } else if (value === 6 && isSlot(props.data)) {
    return (
      <Typography variant="body2" color="text.secondary" align="left">
        <p>
          {props.data.start_time.hour}時{props.data.start_time.minute}分開始
        </p>
        <p>
          {props.data.end_time.hour}時{props.data.end_time.minute}分終了
        </p>
      </Typography>
    );
  } else if (value === 7 && isTask(props.data)) {
    return (
      <Typography variant="body2" color="text.secondary" align="right">
        <p>最低限必要な人数:{props.data.min_worker_num}人</p>{" "}
        <p>
          その中で必要な経験者の数:
          {props.data.exp_worker_num}人
        </p>{" "}
        <p>最大人数:{props.data.max_worker_num}人</p>
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

export const isBid = (data: any): data is BidResponse => {
  return !!(data as BidResponse)?.open_time;
};

export const isSlot = (data: any): data is SlotResponse => {
  return !!(data as SlotResponse)?.start_time;
};

export const isTask = (data: any): data is TaskResponse => {
  return !!(data as TaskResponse)?.max_worker_num;
};

export const isBidder = (data: any): data is BidderResponse => {
  return (
    !!(data as BidderResponse)?.point && !!(data as BidderResponse)?.user_id
  );
};
