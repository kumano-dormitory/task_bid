import React from "react";
import { NavLink, Outlet } from 'react-router-dom'
import PositionedMenu from "./PositionedMenu";
import { Stack } from "@mui/system";
import AccountMenu from "./AcountMenu";
export const Layout: React.FC = () => {
    return (
        <div>
            <ul><Stack direction={'row'}><PositionedMenu /><AccountMenu/></Stack></ul>
            <Outlet />
            <ul>
                <h4>Footer</h4>
            </ul>
        </div>
    )
}