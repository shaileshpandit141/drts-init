import { useState, useEffect, useRef, useCallback } from "react";

interface UseHasTouchedOrPassedTopOptions {
  threshold?: number;
}

export function useHasTouchedOrPassedTop<
  T extends HTMLElement,
  C extends HTMLElement = HTMLDivElement,
>({ threshold = 0 }: UseHasTouchedOrPassedTopOptions = {}) {
  const elementRef = useRef<T | null>(null);
  const scrollContainerRef = useRef<C | null>(null);
  const [hasTouchedOrPassedTop, setHasTouchedOrPassedTop] = useState(false);

  const checkPosition = useCallback(() => {
    if (!elementRef.current || !scrollContainerRef.current) return;

    const elementRect = elementRef.current.getBoundingClientRect();
    const containerRect = scrollContainerRef.current
      ? scrollContainerRef.current.getBoundingClientRect()
      : { top: 0 };

    const isTouchedOrPassed = elementRect.top <= containerRect.top + threshold;
    setHasTouchedOrPassedTop(isTouchedOrPassed);
  }, [threshold]);

  useEffect(() => {
    const container = scrollContainerRef.current || window;

    const handleScroll = () => checkPosition();
    const handleResize = () => checkPosition();

    container.addEventListener("scroll", handleScroll, { passive: true });
    window.addEventListener("resize", handleResize);
    checkPosition(); // Initial check

    return () => {
      container.removeEventListener("scroll", handleScroll);
      window.removeEventListener("resize", handleResize);
    };
  }, [checkPosition]);

  return { elementRef, scrollContainerRef, hasTouchedOrPassedTop };
}
