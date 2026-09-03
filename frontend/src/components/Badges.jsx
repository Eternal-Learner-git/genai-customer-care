import React from "react";

// Coral is reserved for high/critical priority only, so it stays meaningful
// rather than decorative - everything else uses neutral or teal tones.
const PRIORITY_STYLES = {
  low: "bg-teal-50 text-teal-700",
  medium: "bg-amber-50 text-amber-700",
  high: "bg-coral-50 text-coral-500",
  critical: "bg-coral-400 text-white",
};

export function PriorityBadge({ priority }) {
  const style = PRIORITY_STYLES[priority] || "bg-ink/5 text-ink/60";
  return (
    <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${style}`}>
      {priority}
    </span>
  );
}

const STATUS_STYLES = {
  open: "bg-ink/5 text-ink/70",
  in_progress: "bg-teal-50 text-teal-700",
  resolved: "bg-teal-100 text-teal-700",
  closed: "bg-ink/5 text-ink/40",
};

export function StatusBadge({ status }) {
  const style = STATUS_STYLES[status] || "bg-ink/5 text-ink/60";
  const label = status.replace("_", " ");
  return (
    <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${style}`}>
      {label}
    </span>
  );
}
