import * as React from 'react';
import dayjs, { Dayjs } from 'dayjs';
import TextField from '@mui/material/TextField';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker } from '@mui/x-date-pickers';
import { styled } from '@mui/material/styles';
import Chip from '@mui/material/Chip';
import Paper from '@mui/material/Paper';
import { v4 as uuidv4 } from "uuid";
const ListItem = styled('li')(({ theme }) => ({
  margin: theme.spacing(0.5),
}));




export interface Datedata{
  key: string,
  date:Dayjs,
}

type DateMultiSelectProps = {
  days: Datedata[];
  setDays:React.Dispatch<React.SetStateAction<Datedata[]>>
}

export const DateMultiSelect:React.FC<DateMultiSelectProps>=(props:DateMultiSelectProps)=> {
  const [days, setDays] = [props.days,props.setDays]
  const [selectday,setSelected]=React.useState<dayjs.Dayjs|null>()
  const handleDelete = (chipToDelete: Datedata) => () => {
    setDays((chips) => chips.filter((chip) => chip.key !== chipToDelete.key));
  };

  const handleChange = (newValue: Dayjs | null) => {
    setSelected(newValue)
    if (newValue) {
      setDays([...days,{key:uuidv4(),date:newValue}]);
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Paper
      sx={{
        display: 'flex',
        justifyContent: 'center',
        flexWrap: 'wrap',
        listStyle: 'none',
        p: 0.5,
        m: 0,
      }}
      component="ul"
    >
      {days.map((data) => {
        return (
          <ListItem key={data.key}>
            <Chip
              label={data.date.format('YYYY/MM/DD')}
              onDelete={handleDelete(data)}
            />
          </ListItem>
        );
      })}
          <DatePicker
          value={selectday}
          onChange={handleChange}
          onError={console.log}
          minDate={dayjs()}
          inputFormat="YYYY/MM/DD"
          renderInput={(params) => <TextField {...params} />}
        />
    </Paper>
    </LocalizationProvider>
  );
}