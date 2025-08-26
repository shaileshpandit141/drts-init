import React, { FC, JSX } from "react";
import styles from "./Header.module.css";
import { Link } from "react-router-dom";

const Header: FC = (): JSX.Element => {
    return (
        <header className={styles.container}>
            <section className={styles.left}>
                <span className={styles.appTitle}>DrtsInit</span>
            </section>
            <section className={styles.centre}></section>
            <section className={styles.right}>
                <Link to={"/signin"} className={styles.link}>Sign in</Link>
            </section>
        </header>
    )
}

export default Header;
