import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import { getData, TaskResponse } from "../../ResponseType";
import useSWR, { Fetcher } from "swr";
import { ModalBase } from "../modal/ModalBase";
import { TaskModalField } from "../modal/TaskModalField";
const getTask: Fetcher<TaskResponse[]> = (url: string) => {
  return getData(url);
};

export const TaskAllList:React.FC=()=> {
    const { data, error } = useSWR("/tasks/", getTask);
    const [task, setTask] = React.useState<TaskResponse>()
    const [open, setOpen] = React.useState(false);
  if (error) return <div>Loading Failed</div>;
    if (!data) return <div>Loading...</div>;
    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);
    const handleClick = (task:TaskResponse) => {
        setTask(task)
        handleOpen();
    }
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>名前</TableCell>
            <TableCell align="right">最大参加人数</TableCell>
            <TableCell align="right">最小参加人数</TableCell>
            <TableCell align="right">必要な経験者の人数</TableCell>
            <TableCell align="right">最高ポイント</TableCell>
            <TableCell align="right">最低ポイント</TableCell>
            <TableCell align="right">作成者</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((task) => (
            <TableRow
                  key={task.id}
                  onClick={()=>handleClick(task)}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}

            >
              <TableCell component="th" scope="row">
                {task.name}
              </TableCell>
              <TableCell align="right">{task.max_worker_num}</TableCell>
              <TableCell align="right">{task.min_worker_num}</TableCell>
              <TableCell align="right">{task.exp_worker_num}</TableCell>
              <TableCell align="right">{task.start_point}</TableCell>
              <TableCell align="right">{task.buyout_point}</TableCell>
              <TableCell align="right">{task.creater}</TableCell>
            </TableRow>
          ))}
        </TableBody>
          </Table>
          <ModalBase title='詳細' open={open} handleClose={handleClose}>
              <TaskModalField data={task!}/>
          </ModalBase>
    </TableContainer>
  );
}
