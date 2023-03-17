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
import { useLocation} from "react-router-dom";
import { DateMultiSelect } from "../field/DateMultiSelect";
import { Datedata } from "../field/DateMultiSelect";
import { useSnackbar } from "../Snackbar";
import { getData } from "../../ResponseType";
import useSWR from 'swr';
const theme = createTheme();

export const SlotFromTemplate = () => {
  const navigate = useNavigate();
  const [days, setDays] = React.useState<Datedata[]>([]);
  const location = useLocation();
  const [template] = React.useState<{
    template_id: string;
  }>(location.state as { template_id: string;});
  const { data, error } = useSWR(`/templates/${template.template_id}`, getData)
  const {showSnackbar}=useSnackbar()
  if (!data) return <div>Loading...</div>
  if (error) return <div>Loading Failed</div>
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    
    axios
      .post(`/templates/${template.template_id}/generate`, {
        first_days: days.map((day) => {
          return {
            year: day.date.get("year"),
            month: day.date.get("month") + 1,
            day: day.date.get("date"),
          };
        }),
      })
      .then((response) => {
        console.log(response);
        navigate("/bidpage/");
        showSnackbar('作成成功','success')
      })
      .catch((err) => {
        console.log(err);
        showSnackbar('作成失敗','error')

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
            { data.name}からシフトを作成
          </Typography>
          <Box
            component="form"
            noValidate
            onSubmit={handleSubmit}
            sx={{ mt: 3 }}
          >
            <Grid container spacing={2}>
              <Grid>
                <DateMultiSelect days={days} setDays={setDays} />
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
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
};
