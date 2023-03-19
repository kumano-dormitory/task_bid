import * as React from "react";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import axios from "../axios";
import { SlotAllList } from "./list/SlotAllList";
import TemplateRow from "./list/TemplateRow";
import { TaskAllList } from "./list/TaskAllList";
import { CreateCard } from "./field/NewCreateCard";
import { useNavigate } from "react-router-dom";
import { useSnackbar } from "./Snackbar";
export const AdminPage: React.FC = () => {
  const navigate = useNavigate();
  const { showSnackbar } = useSnackbar();
  const handleClick = () => {
    axios
      .post("/admin/closebid")
      .then((response) => {
        showSnackbar("ビッド終了処理成功", "success");
        console.log(response.data);
      })
      .catch((err) => {
        console.log(err);
      });
  };
  const handleDeleteClick = () => {
    axios
      .delete("/slots/")
      .then((response) => {
        console.log(response);
        showSnackbar("削除しました", "success");
      })
      .catch((err) => {
        console.log(err);
        showSnackbar('削除失敗', 'error');
      });
  };
  return (
    <>
      <Stack spacing={2} direction="row">
        <Button variant="text" onClick={handleClick}>
          Close Finished Bids
        </Button>
        <Button variant="text" onClick={handleDeleteClick}>
          Remove unused slots
        </Button>
        <Button variant="contained">Contained</Button>
        <Button variant="outlined">Outlined</Button>
      </Stack>
      <SlotAllList />
      <CreateCard
        text="新しく仕事を募集"
        onClick={() => {
          navigate("/newslot");
        }}
      />
      <TaskAllList />
      <CreateCard
        text="新しいタスクを作成"
        onClick={() => {
          navigate("/newtask");
        }}
      />
      <TemplateRow />
      <CreateCard
        text="テンプレートを作成"
        onClick={() => {
          navigate("/newtemplate");
        }}
      />
    </>
  );
};
