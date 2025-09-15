import React, { FC, JSX } from "react";
import styles from "./Header.module.css";
import { Link } from "react-router-dom";
import ToggleTheme from "components/common/ToggleTheme";
import { useAuth } from "features/auth/hooks";
import Signout from "components/feature/Signout";
import UserProfile from "components/feature/UserProfile";

const Header: FC = (): JSX.Element => {
    const { isAuthenticated } = useAuth();

    return (
        <header className={styles.container}>
            <section className={styles.left}>
                <span className={styles.appTitle}>DrtsInit</span>
            </section>
            <section className={styles.centre}></section>
            <section className={styles.right}>
                {isAuthenticated ? <Signout /> : <Link to={"/sign-in"} className={styles.link}>Sign in</Link>}
                <ToggleTheme />
                <UserProfile />
            </section>
        </header>
    )
}

export default Header;
