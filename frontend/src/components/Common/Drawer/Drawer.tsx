import React, { useState, useEffect, useCallback } from "react";
import "./Drawer.css";

interface DrawerProps {
  children: React.ReactNode;
  isOpen: boolean;
  onClick?: (event: React.MouseEvent<HTMLElement>) => void;
  position?: "fixed" | "absolute";
  className?: string;
  style?: React.CSSProperties;
}

const TRANSITION_DURATION = 300;

const Drawer: React.FC<DrawerProps> = ({
  children,
  onClick,
  isOpen,
  position = "fixed",
  className,
  style,
}): JSX.Element => {
  const [isDeactivated, setIsDeactivated] = useState(false);
  const [isTransitioning, setIsTransitioning] = useState(false);

  const handleTransition = useCallback((shouldDeactivate: boolean) => {
    setIsTransitioning(true);
    if (shouldDeactivate) {
      setIsDeactivated(false);
    }

    const timer = setTimeout(() => {
      setIsTransitioning(false);
      if (!shouldDeactivate) {
        setIsDeactivated(true);
      }
    }, TRANSITION_DURATION);

    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (isOpen) {
      document.documentElement.style.overflow = "hidden";
      handleTransition(true);
    } else {
      document.documentElement.style.overflow = "unset";
      handleTransition(false);
    }
    return () => {
      document.documentElement.style.overflow = "unset";
    };
  }, [isOpen, handleTransition]);

  const handleClick = useCallback(
    (event: React.MouseEvent<HTMLElement>) => {
      if (event.target === event.currentTarget && onClick && !isTransitioning) {
        event.stopPropagation();
        onClick(event);
      }
    },
    [onClick, isTransitioning],
  );

  const drawerClassName = `drawer ${className || ""}
    ${isOpen ? "drawer--active" : "drawer--inactive"}
    ${isDeactivated && !isOpen ? "drawer--inactive" : ""}`;

  return (
    <div
      className={drawerClassName}
      onClick={handleClick}
      style={{ position: position, ...style }}
    >
      {children}
    </div>
  );
};

export default Drawer;
