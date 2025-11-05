import React, { useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";


const Submission = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = () => {
    setIsSubmitting(true);
    const passed = Math.random() > 0.5; // τυχαία επιτυχία/αποτυχία

    setTimeout(() => {
      setIsSubmitting(false);

      if (passed) {
        toast.success("All the test cases passed!", {
          position: "bottom-right",
          autoClose: 3000,
          theme: "colored",
        });
      } else {
        toast.error("Some of the test cases haven’t passed. Try again!", {
          position: "bottom-right",
          autoClose: 3000,
          theme: "colored",
        });
      }
    }, 1500);
  };

  return (
    <div className="submission-container">
      <h1>Submit your solution</h1>

      <button
        onClick={handleSubmit}
        disabled={isSubmitting}
        className="submit-button"
      >
        {isSubmitting ? "Submitting..." : "Submit Solution"}
      </button>

      <ToastContainer />
    </div>
  );
};

export default Submission;
