import React from "react";
import { PriorityBadge, StatusBadge } from "./Badges";

export default function ComplaintCard({ complaint, children }) {
  return (
    <div className="rounded-lg border border-ink/10 bg-white p-5">
      <div className="flex items-start justify-between gap-4">
        <h3 className="font-medium text-ink">{complaint.subject}</h3>
        <div className="flex shrink-0 gap-2">
          <PriorityBadge priority={complaint.priority} />
          <StatusBadge status={complaint.status} />
        </div>
      </div>

      <p className="mt-2 text-sm text-ink/70">{complaint.description}</p>

      {(complaint.category || complaint.sentiment) && (
        <div className="mt-3 flex gap-4 text-xs text-ink/50">
          {complaint.category && <span>Category: {complaint.category}</span>}
          {complaint.sentiment && <span>Sentiment: {complaint.sentiment}</span>}
        </div>
      )}

      {complaint.suggested_response && (
        <div className="mt-3 rounded-md bg-teal-50 p-3 text-sm text-teal-800">
          <span className="font-medium">Suggested response: </span>
          {complaint.suggested_response}
        </div>
      )}

      <p className="mt-3 text-xs text-ink/40">
        Filed {new Date(complaint.created_at).toLocaleDateString()}
      </p>

      {children}
    </div>
  );
}
