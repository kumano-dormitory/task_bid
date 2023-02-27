import * as React from "react";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import { TabUnselected } from "@mui/icons-material";
import { createContext } from "react";
import { BidList } from "./BidList";
interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    "aria-controls": `simple-tabpanel-${index}`,
  };
}

export const UrlContext = createContext('/bids/open');

export const BidPage: React.FC = () => {
  const [value, setValue] = React.useState(0);
  const [url, setURL] = React.useState('/bids/open')
  
  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ width: "100%" }}>
      <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
        <Tabs
          value={value}
          onChange={handleChange}
          aria-label="basic tabs example"
        >
          <Tab label="募集中" onClick={()=>setURL('bids/open')} {...a11yProps(0)} />
          <Tab label="人数不足中" onClick={()=>setURL('bids/lack')} {...a11yProps(1)} />
          <Tab label="完了したシフト" onClick={()=>setURL('bids/open')} {...a11yProps(2)} />
          <Tab label="新規募集" onClick={()=>setURL('bids/open')} {...a11yProps(3)} />
        </Tabs>
      </Box>
      <UrlContext.Provider value={url}>
      <TabPanel value={value} index={0}>
      <BidList/>
      </TabPanel>
      <TabPanel value={value} index={1}>
        人数不足中
      </TabPanel>
      <TabPanel value={value} index={2}>
        終わったシフト
      </TabPanel>
      <TabPanel value={value} index={3}>
        新規募集
        </TabPanel>
        </UrlContext.Provider>
    </Box>
  );
};
