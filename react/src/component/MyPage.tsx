import React, { useState } from "react";
import { UserContext } from "../UserContext";
import { useContext } from "react";
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
import { MenuItem } from "@mui/material";
import { useNavigate } from "react-router-dom";
import axios from "../axios";
import { DateSelect } from "./field/DateSelect";
import dayjs, { Dayjs } from "dayjs";
import { useLocation } from "react-router-dom";
import { Datetime } from "../ResponseType";
import { blocks } from "./form/Register";
import Stack from "@mui/material/Stack";
import Chip from "@mui/material/Chip";
const theme = createTheme();
export const MyPage: React.FC = () => {
  const { user } = useContext(UserContext);
  const [isMatch, setMatch] = useState(false);
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    if (data.get("old_password")) {
      if (data.get("password") !== data.get("repassword")) {
        setMatch(true);
        return;
      }
      axios
        .patch(`/users/${user.id}`, {
          name: data.get("name"),
          block: data.get("block"),
          room_number: data.get("room_number"),
          old_password: data.get("old_password"),
          password: data.get("password"),
        })
        .then((response) => {
          console.log(response.data);
        })
        .catch((err) => {
          console.log(err);
        });
    }
    axios
      .patch(`/users/${user.id}`, {
        name: data.get("name"),
        block: data.get("block"),
        room_number: data.get("room_number"),
      })
      .then((response) => {
        console.log(response.data);
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
          </Avatar>
          <Typography component="h1" variant="h5">
            ユーザー情報
          </Typography>
          <Box
            component="form"
            noValidate
            onSubmit={handleSubmit}
            sx={{ mt: 3 }}
          >
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography component={"h2"} variant="h2">
                  {user.point}
                </Typography>
                <Typography component={"h5"} variant="h5">
                  ポイント
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  autoComplete="given-name"
                  name="name"
                  required
                  fullWidth
                  id="name"
                  label="名前"
                  autoFocus
                  defaultValue={user.name}
                  variant="standard"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  id="room_number"
                  label="部屋番号"
                  name="room_number"
                  autoComplete="room_number"
                  defaultValue={user.room_number}
                  variant="standard"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  id="block"
                  name="block"
                  select
                  label="Block"
                  defaultValue={user.block}
                  variant="standard"
                >
                  {blocks.map((option) => (
                    <MenuItem key={option} value={option}>
                      {option}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  name="old_password"
                  label="old password"
                  type="password"
                  id="old_password"
                  autoComplete="new-password"
                  variant="standard"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  error={isMatch}
                  name="password"
                  label="Password"
                  type="password"
                  id="password"
                  autoComplete="new-password"
                  variant="standard"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  error={isMatch}
                  name="repassword"
                  label="Repeat your password"
                  type="password"
                  id="repassword"
                  autoComplete="new-password"
                  helperText={isMatch ? "Password not match" : ""}
                  variant="standard"
                />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              更新
            </Button>
          </Box>
          <Stack direction="row" spacing={1}>
            {user.exp_task.map((task) => {
              return <Chip label={task.name} />;
            })}
          </Stack>
        </Box>
      </Container>
    </ThemeProvider>
  );
};
