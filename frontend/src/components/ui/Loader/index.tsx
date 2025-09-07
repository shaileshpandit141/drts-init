import React, { FC, JSX } from "react";
import styles from "./Loader.module.css";
import { Loader as L } from "lucide-react";

interface LoaderProps {
    size?: string | number
}

const Loader: FC<LoaderProps> = (props): JSX.Element | null => {
    const { size = "24px" } = props;
    return (
        <div className={styles.container} style={{ height: size }}>
            <span className={styles.loader}><L /></span>
        </div>
    )
}

export default Loader;
