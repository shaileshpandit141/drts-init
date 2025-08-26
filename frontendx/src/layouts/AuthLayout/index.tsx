import React, { FC, JSX } from "react";
import "./AuthLayout.module.css";
import { Outlet } from "react-router-dom";

const AuthLayout: FC = (): JSX.Element => {
    return (
        <main>
            <Outlet />
        </main>
    )
}

export default AuthLayout;
