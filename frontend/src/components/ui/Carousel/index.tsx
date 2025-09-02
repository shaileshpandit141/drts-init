import React, { useState, useEffect, useRef, ReactNode, useCallback } from "react";
import "./Carousel.css";

// Interface defining allowed props for the Carousel component
interface CarouselProps {
  children: ReactNode[]; // Array of child elements to display as slides
  navigation: "none" | "buttons" | "thumbnails" | "dot-thumbnails"; // Navigation style
  slideStatus?: boolean; // Display carousel slide status or not
  infiniteScroll?: boolean; // Enable infinite scrolling
  autoplay?: boolean; // Enable autoplay
  autoplaySpeed?: number; // Autoplay interval in ms
  height?: string;
  maxHeight?: string;
  width?: string;
  maxWidth?: string;
  borderRadius?: number;
}

const Carousel: React.FC<CarouselProps> = ({
  children,
  navigation = "none",
  slideStatus = true,
  infiniteScroll = false,
  autoplay = false,
  autoplaySpeed = 3000,
  height = "fit-content",
  maxHeight = "240px",
  width = "100%",
  maxWidth = "480px",
  borderRadius = 0,
}) => {
  const totalSlides = children.length;
  // Add clone slides at start/end if infinite scroll enabled
  const extendedSlides = infiniteScroll
    ? [children[totalSlides - 1], ...children, children[0]]
    : children;

  // State management for carousel
  const [currentIndex, setCurrentIndex] = useState(infiniteScroll ? 1 : 0); // Start at 1 for infinite scroll
  const [isTransitioning, setIsTransitioning] = useState(false); // Control slide animations
  const [isPaused, setIsPaused] = useState(false); // Pause autoplay on hover
  const trackRef = useRef<HTMLDivElement>(null); // Reference to track element
  const touchStartX = useRef<number | null>(null); // Store touch position for swipe

  // Navigate to next slide
  const nextSlide = useCallback(() => {
    if (!isTransitioning) {
      setIsTransitioning(true);
      setCurrentIndex((prev) => prev + 1);
    }
  }, [isTransitioning]);

  // Handle autoplay functionality
  useEffect(() => {
    if (!autoplay || isPaused) return;
    const interval = setInterval(() => nextSlide(), autoplaySpeed);
    return () => clearInterval(interval);
  }, [autoplay, autoplaySpeed, isPaused, nextSlide]);


  // Navigate to previous slide
  const prevSlide = () => {
    if (!isTransitioning) {
      setIsTransitioning(true);
      setCurrentIndex((prev) => prev - 1);
    }
  };

  // Handle infinite scroll slide transitions
  useEffect(() => {
    if (!infiniteScroll) return;
    const transitionEnd = () => {
      setIsTransitioning(false);
      // Jump to end when reaching start
      if (currentIndex === 0) {
        setCurrentIndex(totalSlides);
      }
      // Jump to start when reaching end
      else if (currentIndex === totalSlides + 1) {
        setCurrentIndex(1);
      }
    };

    const track = trackRef.current;
    if (track) track.addEventListener("transitionend", transitionEnd);
    return () => {
      if (track) track.removeEventListener("transitionend", transitionEnd);
    };
  }, [currentIndex, infiniteScroll, totalSlides]);

  // Touch event handlers for mobile swipe
  const handleTouchStart = (e: React.TouchEvent) => {
    touchStartX.current = e.touches[0].clientX;
  };

  const handleTouchEnd = (e: React.TouchEvent) => {
    if (!touchStartX.current) return;
    const touchEndX = e.changedTouches[0].clientX;
    const deltaX = touchStartX.current - touchEndX;

    // If swipe distance > 50px, change slide
    if (Math.abs(deltaX) > 50) {
      deltaX > 0 ? nextSlide() : prevSlide();
    }
    touchStartX.current = null;
  };

  return (
    <div
      className="carousel"
      style={{
        height: height,
        maxHeight: maxHeight,
        width: width,
        maxWidth: maxWidth,
        borderRadius: borderRadius,
      }}
    >
      <div
        className="carousel-track"
        ref={trackRef}
        onMouseEnter={() => setIsPaused(true)}
        onMouseLeave={() => setIsPaused(false)}
        onTouchStart={handleTouchStart}
        onTouchEnd={handleTouchEnd}
        style={{
          transform: `translateX(-${currentIndex * 100}%)`,
          transition: isTransitioning ? "transform 0.4s ease-in-out" : "none",
        }}
      >
        {extendedSlides.map((child, index) => (
          <div key={index} className="carousel-slide">
            {child}
          </div>
        ))}
      </div>

      {/* Carousel slide status */}
      {slideStatus && (
        <div className="carousel-slide-status">
          <h6 className="status">
            {infiniteScroll
              ? currentIndex === 0
                ? totalSlides
                : currentIndex > totalSlides
                  ? 1
                  : currentIndex
              : currentIndex + 1}
            /{totalSlides}
          </h6>
        </div>
      )}

      {/* Carousel Slide Navigations */}
      {navigation !== "none" && (
        <div
          className="carousel-thumbnail-navigations"
          onMouseEnter={() => setIsPaused(true)}
          onMouseLeave={() => setIsPaused(false)}
          onTouchStart={handleTouchStart}
          onTouchEnd={handleTouchEnd}
        >
          {/* Thumbnail navigation - displays image thumbnails */}
          <div className="thumbnails">
            {(navigation === "thumbnails" ||
              navigation === "dot-thumbnails") && (
                <div className="thumbnails-wrapper">
                  {children.map((child, index) => {
                    let ReactChild = child as React.ReactElement;
                    if (
                      ReactChild.type === "img" &&
                      navigation !== "dot-thumbnails"
                    ) {
                      return (
                        <img
                          key={index}
                          src={(child as React.ReactElement<HTMLImageElement>).props.src}
                          alt={`Thumbnail ${index}`}
                          className={
                            (
                              infiniteScroll
                                ? currentIndex === index + 1 // Adjust for infinite scroll offset
                                : currentIndex === index
                            )
                              ? "active"
                              : ""
                          }
                          onClick={() => {
                            setIsTransitioning(true);
                            setIsPaused(true);
                            setCurrentIndex(infiniteScroll ? index + 1 : index);
                          }}
                        />
                      );
                    }

                    // Dot thumbnail navigation - displays dots for each slide is child is not img tag
                    return (
                      <div
                        key={index}
                        className={
                          (
                            infiniteScroll
                              ? currentIndex === index + 1 // Adjust for infinite scroll offset
                              : currentIndex === index
                          )
                            ? "dot active"
                            : "dot"
                        }
                        onClick={() => {
                          setIsTransitioning(true);
                          setIsPaused(true);
                          setCurrentIndex(infiniteScroll ? index + 1 : index);
                        }}
                      ></div>
                    );
                  })}
                </div>
              )}

            {/* Button navigation - displays prev/next buttons */}
            {navigation === "buttons" && (
              <>
                <div className="prev-slide-button-container">
                  <button
                    className="prev-slide-button"
                    onMouseEnter={() => setIsPaused(true)}
                    onMouseLeave={() => setIsPaused(false)}
                    onTouchStart={handleTouchStart}
                    onTouchEnd={handleTouchEnd}
                    onClick={() => {
                      setIsPaused(true);
                      prevSlide();
                    }}
                    disabled={!infiniteScroll && currentIndex === 0}
                  >
                    <span className="arrow prev"></span>
                  </button>
                </div>
                <div className="next-slide-button-container">
                  <button
                    className="next-slide-button"
                    onMouseEnter={() => setIsPaused(true)}
                    onMouseLeave={() => setIsPaused(false)}
                    onTouchStart={handleTouchStart}
                    onTouchEnd={handleTouchEnd}
                    onClick={() => {
                      setIsPaused(true);
                      nextSlide();
                    }}
                    disabled={
                      !infiniteScroll && currentIndex === totalSlides - 1
                    }
                  >
                    <span className="arrow next"></span>
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Carousel;
