// src/components/CredibilityBar.jsx
import React from "react";

const getColorAndWidth = (verdict) => {
  switch (verdict?.toLowerCase()) {
    case "fake":
      return { color: "bg-red-600", width: "10%" };
    case "soft fake":
      return { color: "bg-orange-500", width: "30%" };
    case "uncertain":
      return { color: "bg-gray-500", width: "50%" };
    case "likely real":
      return { color: "bg-green-500", width: "90%" };
    default:
      return { color: "bg-gray-400", width: "40%" };
  }
};

const CredibilityBar = ({ verdict }) => {
  const { color, width } = getColorAndWidth(verdict);

  return (
    <div className="h-2 w-full bg-muted rounded-full overflow-hidden">
      <div
        className={`h-2 rounded-full transition-all duration-700 ease-in-out ${color}`}
        style={{ width }}
      />
    </div>
  );
};

export default CredibilityBar;
