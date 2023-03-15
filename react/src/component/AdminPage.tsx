import * as React from 'react';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import axios from '../axios';
import { SlotAllList } from './list/SlotAllList';
import TemplateRow from './list/TemplateRow';

export const AdminPage:React.FC=()=> {
    const handleClick = () => {
        axios.post('/admin/closebid').then(
            (response) => {
                console.log(response.data)
            }
        ).catch((err) => {
            console.log(err)
        })
    }
  const handleDeleteClick = () => {
    axios.delete('/slots/').then(
      (response) => {
        console.log(response)
      }
    ).catch((err) => {
      console.log(err)
    })
  }
  return (<>
    <Stack spacing={2} direction="row">
      <Button variant="text" onClick={handleClick}>Close Finished Bids</Button>
      <Button variant="text" onClick={handleDeleteClick}>Remove unused slots</Button>
      <Button variant="contained">Contained</Button>
      <Button variant="outlined">Outlined</Button>
    </Stack>
    <SlotAllList />
    <TemplateRow/>
  </>
  );
}
