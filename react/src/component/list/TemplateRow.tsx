import * as React from "react";
import Chip from "@mui/material/Chip";
import Stack from "@mui/material/Stack";
import useSWR, { Fetcher } from "swr";
import { getData, SlotResponse, TemplateResponse } from "../../ResponseType";
import { SlotInfo } from "../modal/SlotInfo";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import axios from "../../axios";
import { IconButton } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { slotShouldForwardProp } from "@mui/material/styles/styled";
import { ConfirmModal } from "../modal/ConfirmModal";

type TempSlotType = {
  slot: SlotResponse | undefined;
  template: TemplateResponse;
};

const getTemplates: Fetcher<TemplateResponse[]> = (url: string) => {
  return getData(url);
};
export default function TemplateRow() {
  const { data, error } = useSWR("/templates/", getTemplates);
  const [slot, setSlot] = React.useState<SlotResponse>();
  const [template, setTemplate] = React.useState<TemplateResponse>();
  const [open, setOpen] = React.useState(false);
  const [openConfirm, setConfirmOpen] = React.useState(false);
  if (error) return <div>Loading Failed</div>;
  if (!data) return <div>Loading</div>;
  const handleClick = (slot: SlotResponse, template: TemplateResponse) => {
    setSlot(slot);
    setTemplate(template);
    setOpen(true);
  };
  const handleConfirmOpen = (template: TemplateResponse) => {
    setTemplate(template);
    setConfirmOpen(true);
  };

  const handleClose = () => setOpen(false);
  const handleConfirmClose = () => setConfirmOpen(false);
  const handleDelete = () => {
    axios
      .delete(`/templates/${template?.id}/slots/${slot?.id}`)
      .then((response) => {
        console.log(response);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const deleteTemplate = () => {
    axios.delete(`/templates/${template?.id}`).then((response) => {
      console.log(response)
    }).catch((err) => {
      console.log(err);
    })
  }

  return (
    <>
      {" "}
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableBody>
            <TableHead>
              <TableRow>
                <TableCell>名前</TableCell>
                <TableCell align="right">仕事</TableCell>
              </TableRow>
            </TableHead>

            {data.map((template) => {
              return (
                <TableRow>
                  <TableCell>
                    {template.name}
                    <IconButton
                      onClick={() => {
                        handleConfirmOpen(template);
                      }}
                    >
                      <DeleteIcon />
                    </IconButton>{" "}
                  </TableCell>
                  <TableCell>
                    <Stack direction="row" spacing={1}>
                      {template.slots.map((slot) => {
                        return (
                          <Chip
                            label={slot.name}
                            onClick={() => {
                              handleClick(slot, template);
                            }}
                          />
                        );
                      })}
                    </Stack>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
      {slot ? (
        <SlotInfo
          open={open}
          slot={slot}
          handleClose={handleClose}
          handleDelete={handleDelete}
        />
      ) : (
        <></>
      )}
      {template ? (
        <ConfirmModal
          open={openConfirm}
          names={[template.name]}
          text={"このテンプレートを削除します"}
          handleClose={handleConfirmClose}
          handleSubmit={deleteTemplate}
        />
      ) : (
        <></>
      )}
    </>
  );
}
