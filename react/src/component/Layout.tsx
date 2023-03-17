import React from "react";
import { Outlet } from "react-router-dom";
import PositionedMenu from "./PositionedMenu";
import { Stack } from "@mui/system";
import AccountMenu from "./AcountMenu";
import { UserContext } from "../UserContext";
export const Layout: React.FC = () => {
  return (
    <div>
        <Stack direction={"row"}>
          <PositionedMenu />
        </Stack>
      <Outlet />
        <h4>Footer</h4>
    </div>
  );
};
