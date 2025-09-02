import React, {
  useState,
  useRef,
  useEffect,
  useCallback,
  ReactNode,
  JSX,
} from "react";

interface SplitUIProps {
  direction?: "horizontal" | "vertical";
  children: [ReactNode, ReactNode]; // Expect exactly two children
  persistKey?: string | null;
  minResizerLimit?: number;
  maxResizerLimit?: number;
}

const SplitUI: React.FC<SplitUIProps> = ({
  direction = "horizontal",
  children,
  persistKey = null,
  minResizerLimit = 10,
  maxResizerLimit = 90,
}): JSX.Element => {
  const [size, setSize] = useState<number>(() =>
    persistKey ? Number(localStorage.getItem(persistKey)) || 50 : 50,
  );

  const isResizing = useRef<boolean>(false);
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (persistKey) {
      localStorage.setItem(persistKey, size.toString());
    }
  }, [size, persistKey]);

  const handleMove = useCallback(
    (clientX: number, clientY: number) => {
      if (!isResizing.current || !containerRef.current) return;

      const container = containerRef.current;
      const isHorizontal = direction === "horizontal";
      const newSize =
        (((isHorizontal ? clientX : clientY) -
          (isHorizontal ? container.offsetLeft : container.offsetTop)) /
          (isHorizontal ? container.offsetWidth : container.offsetHeight)) *
        100;

      setSize(Math.max(minResizerLimit, Math.min(maxResizerLimit, newSize)));
      window.dispatchEvent(new Event("resize"));
    },
    [direction, minResizerLimit, maxResizerLimit],
  );

  const handleMouseMove = useCallback(
    (e: MouseEvent) => handleMove(e.clientX, e.clientY),
    [handleMove],
  );

  const handleTouchMove = useCallback(
    (e: TouchEvent) => {
      if (e.touches.length > 0) {
        handleMove(e.touches[0].clientX, e.touches[0].clientY);
      }
    },
    [handleMove],
  );

  const handleUp = useCallback(() => {
    isResizing.current = false;
    document.body.style.cursor = "";
    document.removeEventListener("mousemove", handleMouseMove);
    document.removeEventListener("mouseup", handleUp);
    document.removeEventListener("touchmove", handleTouchMove);
    document.removeEventListener("touchend", handleUp);
    window.dispatchEvent(new Event("resize"));
  }, [handleMouseMove, handleTouchMove]);

  const handleDown = useCallback(() => {
    isResizing.current = true;
    document.body.style.cursor =
      direction === "horizontal" ? "ew-resize" : "ns-resize";
    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleUp);
    document.addEventListener("touchmove", handleTouchMove, { passive: false });
    document.addEventListener("touchend", handleUp);
  }, [direction, handleMouseMove, handleUp, handleTouchMove]);

  const styles: Record<string, React.CSSProperties> = {
    splitContainer: {
      width: "100%",
      height: "100%",
      display: "flex",
      userSelect: "none",
      backgroundColor: "transparent",
      flexDirection: direction === "horizontal" ? "row" : "column",
    },
    splitPanel: {
      overflow: "auto",
      background: "transparent",
    },
    splitResizer: {
      background: "#888",
      cursor: direction === "horizontal" ? "ew-resize" : "ns-resize",
      width: direction === "horizontal" ? "5px" : "100%",
      height: direction === "horizontal" ? "auto" : "5px",
      transition: "background 0.2s ease",
    },
  };

  return (
    <div
      ref={containerRef}
      className={`split-container ${direction}`}
      style={styles.splitContainer}
    >
      <div
        className="split-panel"
        style={{ ...styles.splitPanel, flex: `${size}%` }}
      >
        {children[0]}
      </div>

      <div
        className="split-resizer"
        style={styles.splitResizer}
        onMouseDown={handleDown}
        onTouchStart={handleDown}
      />

      <div
        className="split-panel"
        style={{ ...styles.splitPanel, flex: `${100 - size}%` }}
      >
        {children[1]}
      </div>
    </div>
  );
};

export default SplitUI;
