import * as React from 'react';
import { Box, ThemeProvider, createTheme } from '@mui/system';
const theme = createTheme({
  palette: {
    background: {
      paper: '#fff',
    },
    text: {
      primary: '#173A5E',
      secondary: '#46505A',
    },
    action: {
      active: '#001E3C',
    },
    success: {
      dark: '#009688',
    },
  },
});

type CreateCardProps = {
    text: string,
    onClick: () => void
}

export const CreateCard:React.FC<CreateCardProps>= (props:CreateCardProps)=> {
  return (
    <ThemeProvider theme={theme}>
          <Box
              onClick={props.onClick}
              sx={{
            border:"1px dashed blue",
          bgcolor: 'background.paper',
          boxShadow: 1,
          borderRadius: 2,
          p: 2,
          minWidth: 300,
        }}
      >
        <Box sx={{ color: 'text.primary', fontSize: 24, fontWeight: 'medium' }}>
                +  {props.text}
        </Box>
        
      </Box>
    </ThemeProvider>
  );
}