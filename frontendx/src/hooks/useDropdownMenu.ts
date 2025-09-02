import { useState, useEffect, useRef, useCallback, useMemo } from "react";
import { useLocation } from "react-router-dom";

function useVisibleStyles(additionalStyles: React.CSSProperties = {}) {
  return useMemo(
    () => ({
      opacity: 1,
      pointerEvents: "auto",
      ...additionalStyles,
    }),
    [additionalStyles],
  );
}

function useHiddenStyles(additionalStyles: React.CSSProperties = {}) {
  return useMemo(
    () => ({
      opacity: 0,
      pointerEvents: "none",
      ...additionalStyles,
    }),
    [additionalStyles],
  );
}

export function useDropdownMenu(
  visibleExtraStyles: React.CSSProperties = {},
  hiddenExtraStyles: React.CSSProperties = {},
) {
  const buttonRef = useRef<HTMLButtonElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);
  const location = useLocation();

  // Get merged styles (default + extra styles)
  const visibleStyles = useVisibleStyles(visibleExtraStyles);
  const hiddenStyles = useHiddenStyles(hiddenExtraStyles);

  const toggleDropdownMenu = useCallback(() => {
    setIsVisible((prev) => !prev);
  }, []);

  const closeMenu = useCallback(() => {
    setIsVisible(false);
  }, []);

  // Close menu when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      const buttonElement = buttonRef.current;
      if (!buttonElement) return;

      // Ensure the button has a valid class name
      const buttonClass = buttonElement.className.trim();
      if (!buttonClass) return;

      if (
        contentRef.current &&
        !contentRef.current.contains(event.target as Node) &&
        !(event.target as Element).closest(`.${buttonClass.split(" ")[0]}`)
      ) {
        closeMenu();
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [closeMenu]);

  // Apply styles automatically to buttonRef and contentRef
  useEffect(() => {
    if (buttonRef.current) {
      Object.assign(buttonRef.current.style, {
        position: "relative",
      });
    }
    if (contentRef.current) {
      const transition = contentRef.current.style.transition;
      const zIndex = contentRef.current.style.zIndex;

      Object.assign(contentRef.current.style, {
        position: "absolute",
        userSelect: "none",
        zIndex: zIndex ? zIndex : "999",
        transition: `opacity 0.3s ease-in-out, transform 0.3s ease-in-out, ${transition}`,
        ...(isVisible ? visibleStyles : hiddenStyles),
      });
    }
  }, [isVisible, visibleStyles, hiddenStyles]);

  // Close menu on route change
  useEffect(() => {
    closeMenu();
  }, [location, closeMenu]);

  return {
    buttonRef,
    contentRef,
    toggleDropdownMenu,
  };
}
