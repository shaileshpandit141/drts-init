import React, { FC, JSX } from "react";
import "./MainLayout.module.css";
import { Outlet } from "react-router-dom";

const MainLayout: FC = (): JSX.Element => {
    return (
        <main>
            <Outlet />
        </main>
    )
}

export default MainLayout;
