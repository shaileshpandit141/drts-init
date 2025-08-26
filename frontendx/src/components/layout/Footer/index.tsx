import React, { FC, JSX } from "react";
import styles from "./Footer.module.css";

const Footer: FC = (): JSX.Element => {
    return (
        <footer className={styles.container}>
            <h5>Footer</h5>
        </footer>
    )
}

export default Footer;
