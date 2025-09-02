import React, { FC, JSX } from "react";
import styles from "./Loader.module.css";

interface LoaderProps {
    loaderOn?: boolean
    size?: string | number
}

const Loader: FC<LoaderProps> = (props): JSX.Element => {
    const { loaderOn = false, size = "28px" } = props;

    return (
        <div className={styles.container} style={{ height: size }}>
            {loaderOn && <span className={styles.loader}></span>}
        </div>
    )
}

export default Loader;
