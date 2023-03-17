import * as React from "react";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import { UserContext } from "../UserContext";
import { AdminPage } from "./AdminPage";
import { DataList } from "./list/DataList";
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

export const TabContext = React.createContext(0);

export const BidPage: React.FC = () => {
  const [value, setValue] = React.useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };
  const { user } = React.useContext(UserContext);


  return (
    <TabContext.Provider value={value}>
      <Box sx={{ width: "100%" }}>
        <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
          <Tabs
            value={value}
            onChange={handleChange}
            variant="scrollable"
            scrollButtons="auto"
          >
            <Tab label="参加予定の仕事" {...a11yProps(0)} />
            <Tab label="募集中" {...a11yProps(1)} />
            <Tab label="交代申請中" {...a11yProps(2)} />
            <Tab label="人数不足中" {...a11yProps(3)} />
            <Tab label="経験が不足中" {...a11yProps(4)} />
            <Tab label="完了したシフト" {...a11yProps(5)} />
            <Tab label="管理画面（仮）" {...a11yProps(6)} />
          </Tabs>
        </Box>
        <TabPanel value={value} index={0}>
          <DataList url={"/users/" + user.id + "/slots"} />
        </TabPanel>
        <TabPanel value={value} index={1}>
          <DataList url="/bids/" />
        </TabPanel>
        <TabPanel value={value} index={2}>
          <DataList url="/bidders/?is_canceled=True" />
        </TabPanel>
        <TabPanel value={value} index={3}>
          <DataList url="/bids/?lack=True" />
        </TabPanel>
        <TabPanel value={value} index={4}>
          <DataList url="/bids/?lack_exp=True" />
        </TabPanel>
        <TabPanel value={value} index={5}>
          <DataList url={"/users/" + user.id + "/slots/?end=True"} />
        </TabPanel>
        <TabPanel value={value} index={6}>
          <AdminPage />
        </TabPanel>
      </Box>
    </TabContext.Provider>
  );
};
