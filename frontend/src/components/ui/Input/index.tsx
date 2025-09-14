import React, { FC, JSX } from "react";
import styles from "./Input.module.css";
import clsx from "clsx";

interface InputProps {
    container?: React.HTMLAttributes<HTMLDivElement>,
    label?: {
        left?: string | JSX.Element;
        right?: string | JSX.Element;
    };
    input?: React.InputHTMLAttributes<HTMLInputElement>
}

const Input: FC<InputProps> = (props): JSX.Element => {
    const { container, label, input } = props;

    const getLabel = (label: string | JSX.Element | undefined) => {
        if (label) {
            if (typeof label === "string") {
                return <label>{label}</label>;
            } else {
                return label;
            }
        }
    }

    return (
        <div
            {...container}
            className={clsx(styles.container, container?.className)}
        >
            <div className={styles.labelContainer}>
                {getLabel(label?.left)}
                {getLabel(label?.right)}
            </div>
            <input
                {...input}
                className={clsx(styles.input, input?.className)}
            />
        </div >
    );
};

export default Input;
