import React, { FC, JSX } from "react";
import styles from "./Button.module.css";

interface ButtonProps {
    children?: string | JSX.Element;
    icon?: {
        left?: JSX.Element,
        right?: JSX.Element
    };
    title?: string;
    className?: string;
    onClick?: React.MouseEventHandler<HTMLButtonElement>;
    disabled?: boolean;
    type?: "submit" | "button"


}

const Button: FC<ButtonProps> = (props): JSX.Element | null => {
    const { children, icon, title, className, onClick, disabled = false, type = "button" } = props;

    const setTitle = () => {
        if (!title && typeof children === "string") {
            return children;
        }
        return title
    }

    return (
        <button
            className={`${styles.button} ${className}`}
            title={setTitle()}
            onClick={onClick}
            disabled={disabled}
            type={type}
        >
            <span className={styles.icon}>
                {icon && icon.left}
            </span>
            {children && (
                <span className={styles.text}>{children}</span>
            )}
            <span className={styles.icon}>
                {icon && icon.right}
            </span>
        </button>
    )
}

export default Button;
