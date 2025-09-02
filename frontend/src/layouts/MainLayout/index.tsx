import React, { FC, JSX } from "react";
import styles from "./MainLayout.module.css";
import { Outlet } from "react-router-dom";
import Header from "components/layout/Header";
import Footer from "components/layout/Footer";

const MainLayout: FC = (): JSX.Element => {
    return (
        <main className={styles.container}>
            <Header />
            <div className={styles.content}>
                <Outlet />
            </div>
            <Footer />
        </main>
    )
}

export default MainLayout;
