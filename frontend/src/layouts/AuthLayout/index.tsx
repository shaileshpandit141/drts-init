import React, { FC, JSX } from "react";
import styles from "./AuthLayout.module.css";
import { Outlet } from "react-router-dom";

const AuthLayout: FC = (): JSX.Element => {
    return (
        <main className={styles.container}>
            <Outlet />
        </main>
    )
}

export default AuthLayout;
