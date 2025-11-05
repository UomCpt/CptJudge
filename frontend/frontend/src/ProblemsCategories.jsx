import React, { useState } from "react";
import "./ProblemsCategories.css";

const ProblemsCategories = ({ onFilterChange }) => {
  // κρατάμε ποιο φίλτρο είναι ενεργό
  const [activeCategory, setActiveCategory] = useState("all");

  // όταν πατάει ο χρήστης ένα κουμπί/κάρτα
  const handleCategoryClick = (category) => {
    setActiveCategory(category);
    if (onFilterChange) {
      onFilterChange(category);
    }
  };

  return (
    // wrapper για τις κάρτες φίλτρων
    <div className="card-container">
      {/* Κάρτα για "All Problems" */}
      <div
        className={`card ${activeCategory === "all" ? "active" : ""}`}
        onClick={() => handleCategoryClick("all")}
      >
        All Problems
      </div>

      {/* Κάρτα για "Solved Problems" */}
      <div
        className={`card ${activeCategory === "solved" ? "active" : ""}`}
        onClick={() => handleCategoryClick("solved")}
      >
        Solved Problems
      </div>

      {/* Κάρτα για "Unsolved Problems" */}
      <div
        className={`card ${activeCategory === "unsolved" ? "active" : ""}`}
        onClick={() => handleCategoryClick("unsolved")}
      >
        Unsolved Problems
      </div>
    </div>
  );
};

export default ProblemsCategories;
