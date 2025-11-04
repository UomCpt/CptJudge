import React, { useState } from "react";
import "./ProblemsCategories.css";

const ProblemsCategories = () => {
  // Κατάσταση φίλτρου (all, solved, unsolved)
  const [filter, setFilter] = useState("all");

  // Παραδείγματα προβλημάτων
  const problems = [
    { id: 1, title: "Problem 1 Solved", status: "solved" },
    { id: 2, title: "Problem 2 Unsolved", status: "unsolved" },
    { id: 3, title: "Problem 3 Solved", status: "solved" },
    { id: 4, title: "Problem 4 Unsolved", status: "unsolved" },
  ];

  // Εφαρμόζουμε φίλτρο
  const filtered = problems.filter((p) =>
    filter === "all" ? true : p.status === filter
  );

  return (
    <div className="problems-page">
      {/* Τίτλος */}
      <h1 className="title">Problems</h1>

      {/* Κάρτες φίλτρων */}
      <div className="card-container">
        <div
          onClick={() => setFilter("all")}
          className={`card ${filter === "all" ? "active" : ""}`}
        >
          All Problems
        </div>
        <div
          onClick={() => setFilter("solved")}
          className={`card ${filter === "solved" ? "active" : ""}`}
        >
          Solved Problems
        </div>
        <div
          onClick={() => setFilter("unsolved")}
          className={`card ${filter === "unsolved" ? "active" : ""}`}
        >
          Unsolved Problems
        </div>
      </div>

      {/* Λίστα προβλημάτων */}
      <div className="problem-list">
        {filtered.map((p) => (
          <div
            key={p.id}
            className={`problem ${p.status === "solved" ? "solved" : "unsolved"}`}
          >
            {p.title}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProblemsCategories;
