import * as React from "react";
import Button from "@mui/material/Button";
import { TaskResponse } from "../../ResponseType";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import { Box } from "@mui/material";
import { SimpleChoiceField } from "../field/SimpleChoiceField";
import axios from "../../axios";
import { useSnackbar } from "../Snackbar";
import { ResponseCardProps } from "../field/ResponseCard";
import { useSWRConfig } from "swr";

export const TaskModalField: React.FC<ResponseCardProps<TaskResponse>> = (
  props: ResponseCardProps<TaskResponse>
) => {
  const { showSnackbar } = useSnackbar();
  const [tag_id, setTagID] = React.useState<string[]>([]);
  const [auth_id, setAuthID] = React.useState<string[]>([]);
  const { mutate } = useSWRConfig();

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    axios
      .patch(`/tasks/${props.data.id}`, {
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
        showSnackbar("更新成功", "success");
        mutate('/tasks/')
      })
      .catch((err) => {
        showSnackbar("更新失敗", "error");
        console.log(err);
      });
  };
  const handleTaskDelete = () => {
    axios.delete(`/tasks/${props.data.id}`).then(
      (response) => {
        console.log(response)
        showSnackbar('削除しました', 'success')
      }
    ).catch((err) => {
      showSnackbar('削除失敗','error');
      console.log(err)
    })
    
  }
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
            defaultValue={props.data.name}
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
            defaultValue={props.data.detail}
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            id="max_woker_num"
            name="max_woker_num"
            inputProps={{ min: "1", step: "1" }}
            label="最大人数"
            defaultValue={props.data.max_worker_num}
            type="number"
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            id="min_woker_num"
            name="min_woker_num"
            inputProps={{ min: "1", step: "1" }}
            label="最小人数"
            defaultValue={props.data.min_worker_num}
            type="number"
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            id="exp_woker_num"
            name="exp_woker_num"
            inputProps={{ min: "0", step: "1" }}
            label="必要な経験者の人数"
            defaultValue={props.data.exp_worker_num}
            type="number"
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            id="start_point"
            name="start_point"
            inputProps={{ min: "1", step: "1" }}
            label="開始ポイント"
            defaultValue={props.data.start_point}
            type="number"
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            id="buyout_point"
            name="buyout_point"
            inputProps={{ min: "0", step: "1" }}
            label="即決価格"
            defaultValue={props.data.buyout_point}
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
      <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
      情報更新
      </Button>
      <Button onClick={handleTaskDelete}>タスクを削除する</Button>
    </Box>
  );
};
