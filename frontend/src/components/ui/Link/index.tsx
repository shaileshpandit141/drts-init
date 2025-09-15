import React, { AnchorHTMLAttributes, FC, JSX } from "react";
import styles from "./Link.module.css";
import clsx from "clsx";
import { Link as Alink } from "react-router-dom";

interface LinkProps extends AnchorHTMLAttributes<HTMLAnchorElement> {
    to: string;
    icon?: {
        left?: JSX.Element,
        right?: JSX.Element
    };
}

const Link: FC<LinkProps> = (props): JSX.Element | null => {
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
        <Alink
            {...rest}
            to={rest.to || ""}
            className={clsx(styles.link, rest.className)}
        >
            {renderIcon()[0]}
            <span className={styles.text}>{children}</span>
            {renderIcon()[1]}
        </Alink>
    )
}

export default Link;
