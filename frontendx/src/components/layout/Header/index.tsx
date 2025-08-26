import React, { FC, JSX } from "react";
import styles from "./Header.module.css";
import { Link } from "react-router-dom";
import ToggleTheme from "components/common/ToggleTheme";

const Header: FC = (): JSX.Element => {
    return (
        <header className={styles.container}>
            <section className={styles.left}>
                <span className={styles.appTitle}>DrtsInit</span>
            </section>
            <section className={styles.centre}></section>
            <section className={styles.right}>
                <Link to={"/signin"} className={styles.link}>Sign in</Link>
                <ToggleTheme />
            </section>
        </header>
    )
}

export default Header;
