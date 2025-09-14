import React, { FC, ReactNode, HTMLAttributes, InputHTMLAttributes, useCallback } from "react";
import clsx from "clsx";
import styles from "./Input.module.css";

interface InputProps {
    container?: HTMLAttributes<HTMLDivElement>;
    label?: {
        left?: string | ReactNode;
        right?: string | ReactNode;
    };
    input?: InputHTMLAttributes<HTMLInputElement>;
}

const Input: FC<InputProps> = React.memo(({ container = {}, label = {}, input = {} }) => {
    const renderLabel = useCallback(
        (content?: string | ReactNode) =>
            content ? (typeof content === "string" ? <label>{content}</label> : content) : null,
        []
    );

    return (
        <div {...container} className={clsx(styles.container, container.className)}>
            <div className={styles.labelContainer}>
                {renderLabel(label.left)}
                {renderLabel(label.right)}
            </div>
            <input {...input} className={clsx(styles.input, input.className)} />
        </div>
    );
});

export default Input;
