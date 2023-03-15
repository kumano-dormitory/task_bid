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

export const TemplateForm = () => {
  const navigate = useNavigate();
  const [slots_id, setSlotID] = React.useState<string[]>([]);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    axios
      .post("/templates/", {
        name: data.get("name"),
        slots: slots_id
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
          テンプレートを新規作成
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
              <Grid>
                <SimpleChoiceField
                  url="/slots/"
                  title="仕事"
                  id={slots_id}
                  setData={setSlotID}
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
