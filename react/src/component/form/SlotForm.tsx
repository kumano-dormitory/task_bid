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
import { SingleChoiceField } from "../field/SIngleChoiceField";
import dayjs, { Dayjs } from "dayjs";
import Link from "@mui/material/Link";

const theme = createTheme();

export const SlotForm = () => {
  const navigate = useNavigate();
  const [starttime, setStarttime] = React.useState<Dayjs | null>(dayjs());
  const [endtime, setEndtime] = React.useState<Dayjs | null>(dayjs());

  const [task_id, setTask] = React.useState<string>("None");
  if (!starttime) return <div>Loading</div>;
  if (!endtime) return <div>Loading</div>;
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    axios
      .post("/slots/", {
        name: data.get("name"),
        start_time: {
          year: starttime.get("year"),
          month: starttime.get("month")+1,
          day: starttime.get("date"),
          hour: starttime.get("hour"),
          minute: starttime.get("minute"),
        },
        end_time: {
          year: endtime.get("year"),
          month: endtime.get("month")+1,
          day: endtime.get("date"),
          hour: endtime.get("hour"),
          minute: endtime.get("minute"),
        },
        task_id: task_id,
      })
      .then((response) => {
        console.log(response);
        navigate("/newbid", {
          state: {
            slot_id: response.data.id,
            name: response.data.name,
            start_time: response.data.start_time,
          },
        });
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
            仕事を新規募集
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
                  setOther={{ setOther: setEndtime, timedelta:1,unit:"h"}}
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
                  id={task_id}
                  setData={setTask}
                />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              募集をかける
            </Button>
            <Grid container>
              <Grid item>
                <Link onClick={() => navigate("/selecttemplate")} variant="body2">
                  {"テンプレートからシフトを作成"}
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
};
