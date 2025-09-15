import React, { ButtonHTMLAttributes, FC, JSX } from "react";
import styles from "./Button.module.css";
import clsx from "clsx";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    icon?: {
        left?: JSX.Element,
        right?: JSX.Element
    };
}

const Button: FC<ButtonProps> = (props): JSX.Element | null => {
    const { children, icon, ...rest } = props;

    const renderIcon = (): (JSX.Element | undefined)[] => {
        if (icon) {
            if (icon.left && icon.right) {
                return [
                    <span className={styles.icon}>{icon.left}</span>,
                    <span className={styles.icon}>{icon.right}</span>,
                ];
            } else if (icon.left) {
                return [
                    <span className={styles.icon}>{icon.left}</span>,
                    <span className={styles.icon}></span>,
                ];
            } else if (icon.right) {
                return [
                    undefined,
                    <span className={styles.icon}></span>,
                    <span className={styles.icon}>{icon.right}</span>,
                ];
            }
        }
        return [undefined, undefined]
    }

    return (
        <button
            {...rest}
            className={clsx(styles.button, rest.className)}
        >
            {renderIcon()[0]}
            <span className={styles.text}>{children}</span>
            {renderIcon()[1]}
        </button>
    )
}

export default Button;
