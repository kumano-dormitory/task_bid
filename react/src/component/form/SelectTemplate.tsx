import * as React from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { useNavigate } from "react-router-dom";
import { SingleChoiceField } from "../field/SIngleChoiceField";
import { useSnackbar } from "../Snackbar";
const theme = createTheme();

export const SelectTemplate = () => {
  const navigate = useNavigate();
  const [template_id, setID] = React.useState<string>("");
  const { showSnackbar } = useSnackbar();
  const handleonClick = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    console.log("buttonclicked");
    if (template_id === "") {
      showSnackbar("使用するテンプレートを選択してください", "error");
      return;
    }
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
          <Box component="form" noValidate sx={{ mt: 3 }}>
            <Grid container spacing={2}>
              <SingleChoiceField
                url="/templates/"
                title="テンプレートを選択"
                id={template_id}
                setData={setID}
              />
            </Grid>
            <Button
              onClick={() => {
                template_id === ""
                  ? showSnackbar(
                      "使用するテンプレートを選択してください",
                      "error"
                    )
                  : navigate("/fromtemp", {
                      state: {
                        template_id: template_id,
                      },
                    });
              }}
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              詳細設定へ進む
            </Button>
            {template_id}
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
};
