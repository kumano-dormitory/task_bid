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
import { SimpleChoiceField } from "../field/SimpleChoiceField";
const theme = createTheme();

export const TaskForm = () => {
  const navigate = useNavigate();
  const [tag_id, setTagID] = React.useState<string[]>([]);
  const [auth_id, setAuthID] = React.useState<string[]>([]);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    axios
      .post("/tasks/", {
        name: data.get("name"),
        detail: data.get("detail"),
        max_woker_num: data.get("max_woker_num"),
        min_woker_num: data.get("min_woker_num"),
        exp_woker_num: data.get("exp_woker_num"),
        start_point: data.get("start_point"),
        buyout_point: data.get("buyout_point"),
        tag: tag_id,
        authority: auth_id,
      })
      .then((response) => {
        console.log(response);
        navigate("/bidpage");
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
            タスク新規作成
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
              <Grid item xs={12}>
                <TextField
                  name="detail"
                  maxRows={10}
                  required
                  id="detail"
                  label="説明"
                  fullWidth
                  margin="normal"
                  multiline
                  variant="outlined"
                  placeholder="400字以内"
                  inputProps={{maxLength:400}}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  id="max_woker_num"
                  name="max_woker_num"
                  inputProps={{ min: "1", step: "1" }}
                  label="最大人数"
                  defaultValue="1"
                  type="number"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  id="min_woker_num"
                  name="min_woker_num"
                  inputProps={{ min: "1", step: "1" }}
                  label="最小人数"
                  defaultValue="1"
                  type="number"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  id="exp_woker_num"
                  name="exp_woker_num"
                  inputProps={{ min: "0", step: "1" }}
                  label="必要な経験者の人数"
                  defaultValue="1"
                  type="number"
                />
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
              <Grid>
                <SimpleChoiceField
                  url="/tags"
                  title="タグ"
                  id={tag_id}
                  setData={setTagID}
                />
              </Grid>
              <Grid>
                <SimpleChoiceField
                  url="/authority"
                  title="権限"
                  id={auth_id}
                  setData={setAuthID}
                />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              新規作成
            </Button>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
};
