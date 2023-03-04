import * as React from 'react';
import dayjs, { Dayjs } from 'dayjs';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { SettingsBluetoothRounded } from '@mui/icons-material';



type setOther = {
  setOther: React.Dispatch<React.SetStateAction<dayjs.Dayjs | null>>;
  timedelta: number;
  unit: "h"|"d"|"M"|"y";
}

type DateSelectProps = {
  title: string;
    date: Dayjs | null;
  setValue: React.Dispatch<React.SetStateAction<dayjs.Dayjs | null>>
  setOther?:setOther
}

export const DateSelect:React.FC<DateSelectProps>=(props:DateSelectProps)=> {
  const [value, setValue] = [props.date,props.setValue]

  const handleChange = (newValue: Dayjs | null) => {
    setValue(newValue);
    if (props.setOther) {
      if (newValue) {
        props.setOther.setOther(newValue.add(props.setOther.timedelta,props.setOther.unit))
      }
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Stack spacing={3}>
        <DateTimePicker
          label={props.title}
          value={value}
          onChange={handleChange}
          onError={console.log}
          
          minDate={dayjs()}
          inputFormat="YYYY/MM/DD HH:mm "
          ampm={false}
          renderInput={(params) => <TextField {...params} />}
        />
      </Stack>
    </LocalizationProvider>
  );
}