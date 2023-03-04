import * as React from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { useNavigate } from "react-router-dom";
import axios from "../../axios";
import { DateSelect } from "../field/DateSelect";
import dayjs, { Dayjs } from "dayjs";
import { useLocation } from "react-router-dom";
import { Datetime } from "../../ResponseType";
const theme = createTheme();

export const BidForm: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [slot] = React.useState<{
    slot_id: string;
    name: string;
    start_time: Datetime;
  }>(location.state as { slot_id: string; name: string; start_time: Datetime });
  const [opentime, setOpentime] = React.useState<Dayjs | null>(dayjs());
  const start_time_string=`${slot.start_time.year}-${slot.start_time.month}-${slot.start_time.day}`
  const [closetime, setClocetime] = React.useState<Dayjs | null>(dayjs(start_time_string).subtract(1,'d'));

  if (!opentime) return <div>Loading</div>;
  if (!closetime) return <div>Loading</div>;
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    axios
      .post("/bids/", {
        name: data.get("name"),
        open_time: {
          year: opentime.get("year"),
          month: opentime.get("month")+1,
          day: opentime.get("date"),
          hour: opentime.get("hour"),
          minute: opentime.get("minute"),
        },
        close_time: {
          year: closetime.get("year"),
          month: closetime.get("month")+1,
          day: closetime.get("date"),
          hour: closetime.get("hour"),
          minute: closetime.get("minute"),
        },
        slot: slot.slot_id,
        start_point: data.get("start_point"),
        buyout_point: data.get("buyout_point"),
      })
      .then((response) => {
        console.log(response);
        navigate("/login");
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            募集内容
          </Typography>
          <Box
            component="form"
            noValidate
            onSubmit={handleSubmit}
            sx={{ mt: 3 }}
          >
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  autoComplete="given-name"
                  name="name"
                  defaultValue={`${slot.start_time.month}月${slot.start_time.day}日${slot.name}`}
                  required
                  fullWidth
                  id="name"
                  label="名前"
                  autoFocus
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <DateSelect
                  title="募集開始時刻"
                  date={opentime}
                  setValue={setOpentime}
                />
              </Grid>
              <Grid item xs={12}>
                <DateSelect
                  title="募集停止時刻"
                  date={closetime}
                  setValue={setClocetime}
                />
              </Grid>
              <Grid>
                <Typography component="h1" variant="h6">
                  募集する仕事:{slot.name}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  id="start_point"
                  name="start_point"
                  inputProps={{ min: "1", step: "1" }}
                  label="開始ポイント"
                  defaultValue="10"
                  type="number"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  id="buyout_point"
                  name="buyout_point"
                  inputProps={{ min: "0", step: "1" }}
                  label="即決価格"
                  defaultValue="0"
                  type="number"
                />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              作成完了
            </Button>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
};
