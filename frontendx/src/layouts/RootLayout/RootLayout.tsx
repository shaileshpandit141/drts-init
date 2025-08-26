import React, { FC, JSX } from "react";
import "./RootLayout.module.css";
import { Outlet } from "react-router-dom";

const RootLayout: FC = (): JSX.Element => {
    return <Outlet />
}

export default RootLayout;
