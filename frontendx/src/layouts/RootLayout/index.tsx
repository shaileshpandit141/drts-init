import React, { FC, JSX } from "react";
import styles from "./RootLayout.module.css";
import { Outlet } from "react-router-dom";
import ToggleTheme from "components/common/ToggleTheme";

const RootLayout: FC = (): JSX.Element => {
    return (
        <>
            <div className={styles.themeButton}>
                <ToggleTheme />
            </div>
            <Outlet />
        </>
    )
}

export default RootLayout;
