import React from "react";

const CircularProgress = ({ progress = 0 }) => {
  const radius = 55;
  const stroke = 8;
  const normalizedRadius = radius - stroke * 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center w-[140px] h-[140px] relative">
      {/* Gradient defs */}
      <svg width="0" height="0">
        <defs>
          <linearGradient id="progressGradient" x1="1" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#c084fc" />
            <stop offset="100%" stopColor="#8b5cf6" />
          </linearGradient>
        </defs>
      </svg>

      <svg height={radius * 2} width={radius * 2} className="rotate-[-90deg] absolute">
        {/* Invisible base circle */}
        <circle
          stroke="transparent"
          fill="transparent"
          strokeWidth={stroke}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
        {/* Animated gradient stroke */}
        <circle
          stroke="url(#progressGradient)"
          fill="transparent"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={`${circumference} ${circumference}`}
          style={{
            strokeDashoffset,
            transition: "stroke-dashoffset 0.6s ease-in-out",
            filter: progress === 100 ? "drop-shadow(0 0 6px #a78bfa)" : "none",
          }}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
      </svg>

      {/* Centered Percentage */}
      <span className="text-sm font-medium text-violet-400 z-10">
        {Math.round(progress)}%
      </span>
    </div>
  );
};

export default CircularProgress;
