import React, { ButtonHTMLAttributes, FC, JSX } from "react";
import styles from "./IconButton.module.css";
import clsx from "clsx";

const IconButton: FC<ButtonHTMLAttributes<HTMLButtonElement>> = (props): JSX.Element | null => {
    const { children, ...rest } = props;

    return (
        <button
            {...rest}
            className={clsx(styles.button, rest.className)}
        >
            <span className={styles.iconContainer}>{children}</span>
        </button>
    )
}

export default IconButton;
