import * as React from "react";
import Button from "@mui/material/Button";
import { ResponseBase, SlotResponse } from "../../ResponseType";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import { SingleChoiceField } from "../field/SIngleChoiceField";
import { DateSelect } from "../field/DateSelect";
import { Box } from "@mui/material";
import dayjs, { Dayjs } from "dayjs";
import axios from "../../axios";
import { useSnackbar } from "../Snackbar";
import { useSWRConfig } from "swr";
export type ResponseCardProps<T extends ResponseBase> = {
  data: T;
};

export const SlotModalField: React.FC<ResponseCardProps<SlotResponse>> = (
  props: ResponseCardProps<SlotResponse>
) => {
  const numParse = (number: number) => {
    return number >= 10 ? `${number}` : `0${number}`;
  };
  const { showSnackbar } = useSnackbar();
  const { mutate } = useSWRConfig();
  const start_time_string = `${props.data.start_time.year}-${
    props.data.start_time.month
  }-${props.data.start_time.day} ${numParse(
    props.data.start_time.hour
  )}:${numParse(props.data.start_time.minute)}:00`;
  const end_time_string = `${props.data.end_time.year}-${
    props.data.end_time.month
  }-${props.data.end_time.day} ${numParse(props.data.end_time.hour)}:${numParse(
    props.data.end_time.minute
  )}:00`;
  const [starttime, setStarttime] = React.useState<Dayjs | null>(
    dayjs(start_time_string)
  );
  const [endtime, setEndtime] = React.useState<Dayjs | null>(
    dayjs(end_time_string)
  );
  const [id, setID] = React.useState<string>(props.data.task.id);
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
      const data = new FormData(event.currentTarget);
      console.log(starttime);
    axios
      .patch(`/slots/${props.data.id}`, {
        name: data.get("name"),
        start_time: {
          year: starttime ? starttime.get("year") : props.data.start_time.year,
          month: starttime
            ? starttime.get("month") + 1
            : props.data.start_time.month,
          day: starttime ? starttime.get("date") : props.data.start_time.day,
          hour: starttime ? starttime.get("hour") : props.data.start_time.hour,
          minute: starttime
            ? starttime.get("minute")
            : props.data.start_time.minute,
        },
        end_time: {
          year: endtime ? endtime.get("year") : props.data.end_time.year,
          month: endtime ? endtime.get("month") + 1 : props.data.end_time.month,
          day: endtime ? endtime.get("date") : props.data.end_time.day,
          hour: endtime ? endtime.get("hour") : props.data.end_time.hour,
          minute: endtime ? endtime.get("minute") : props.data.end_time.minute,
        },
        task_id: id,
      })
      .then((response) => {
        console.log(response);
        showSnackbar("更新成功", "success");
        mutate('/slots/')
      })
      .catch((err) => {
        showSnackbar("更新失敗", "error");
        console.log(err);
      });
  };
  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <TextField
            autoComplete="given-name"
            name="name"
            required
            fullWidth
            id="name"
            label="名前"
            defaultValue={props.data.name}
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
          <DateSelect
            title="終了予定時刻"
            date={endtime}
            setValue={setEndtime}
          />
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
      <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
        情報を更新
      </Button>
    </Box>
  );
};
