import * as React from "react";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import useSWR, { Fetcher } from "swr";
import { getData, ResponseBase } from "../../ResponseType";
type SingleChoiceFieldProps = {
  url: string;
  title: string;
  id: string;
  setData: React.Dispatch<React.SetStateAction<string>>;
};

export function SingleChoiceField<T extends ResponseBase>(
  props: SingleChoiceFieldProps
) {
  const [id, setData] = [props.id, props.setData];
  const getChoice: Fetcher<T[]> = getData;
  const { data, error } = useSWR(props.url, getChoice);
  if (error) return <div>Loading Failed</div>;
  if (!data) return <div>Notask </div>;
  const handleChange = (event: SelectChangeEvent) => {
    setData(event.target.value);
  };

  return (
    <div>
      <FormControl sx={{ m: 1, minWidth: 120 }}>
        <InputLabel id="demo-simple-select-helper-label">
          {props.title}
        </InputLabel>
        <Select
          labelId="demo-simple-select-helper-label"
          id="demo-simple-select-helper"
          value={id}
          label={props.title}
          onChange={handleChange}
        >
          {data.map((data) => (
            <MenuItem value={data.id}>{data.name}</MenuItem>
          ))}
        </Select>
      </FormControl>
    </div>
  );
}
