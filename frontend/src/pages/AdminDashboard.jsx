import React, { useEffect, useState } from "react";
import apiClient from "../api/client";
import { PriorityBadge, StatusBadge } from "../components/Badges";

const STATUS_OPTIONS = ["open", "in_progress", "resolved", "closed"];
const PRIORITY_OPTIONS = ["low", "medium", "high", "critical"];

export default function AdminDashboard() {
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [savingId, setSavingId] = useState(null);

  async function loadComplaints() {
    setLoading(true);
    try {
      const res = await apiClient.get("/complaints");
      setComplaints(res.data);
    } catch {
      setError("Couldn't load complaints. Are you logged in as an admin?");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadComplaints();
  }, []);

  async function updateComplaint(id, updates) {
    setSavingId(id);
    try {
      const res = await apiClient.patch(`/complaints/${id}`, updates);
      setComplaints((prev) => prev.map((c) => (c.id === id ? res.data : c)));
    } catch {
      setError("Couldn't save that change. Please try again.");
    } finally {
      setSavingId(null);
    }
  }

  const visibleComplaints =
    statusFilter === "all"
      ? complaints
      : complaints.filter((c) => c.status === statusFilter);

  return (
    <div className="mx-auto max-w-4xl px-6 py-10">
      <div className="flex items-center justify-between">
        <h1 className="font-display text-3xl text-teal-700">All complaints</h1>

        <div className="flex items-center gap-3">
          <button onClick={loadComplaints} className="text-sm text-teal-600 hover:underline">
            Refresh
          </button>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="rounded-md border border-ink/15 px-3 py-1.5 text-sm"
          >
            <option value="all">All statuses</option>
            {STATUS_OPTIONS.map((s) => (
              <option key={s} value={s}>
                {s.replace("_", " ")}
              </option>
            ))}
          </select>
        </div>
      </div>

      {error && <p className="mt-4 text-sm text-coral-500">{error}</p>}

      {loading ? (
        <p className="mt-6 text-sm text-ink/50">Loading…</p>
      ) : visibleComplaints.length === 0 ? (
        <p className="mt-6 text-sm text-ink/50">No complaints match this filter.</p>
      ) : (
        <div className="mt-6 space-y-4">
          {visibleComplaints.map((c) => (
            <div key={c.id} className="rounded-lg border border-ink/10 bg-white p-5">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h3 className="font-medium text-ink">{c.subject}</h3>
                  <p className="mt-1 text-sm text-ink/70">{c.description}</p>
                  <p className="mt-2 text-xs text-ink/50">
                    Filed by <span className="font-medium text-ink/70">{c.owner.name}</span> ({c.owner.email})
                  </p>
                </div>
                <div className="flex shrink-0 gap-2">
                  <PriorityBadge priority={c.priority} />
                  <StatusBadge status={c.status} />
                </div>
              </div>

              {(c.category || c.sentiment) && (
                <div className="mt-3 flex gap-4 text-xs text-ink/50">
                  {c.category && <span>Category: {c.category}</span>}
                  {c.sentiment && <span>Sentiment: {c.sentiment}</span>}
                </div>
              )}

              {c.suggested_response && (
                <div className="mt-3 rounded-md bg-teal-50 p-3 text-sm text-teal-800">
                  <span className="font-medium">Suggested response: </span>
                  {c.suggested_response}
                </div>
              )}

              <div className="mt-4 flex flex-wrap items-center gap-3 border-t border-ink/5 pt-4">
                <label className="text-xs font-medium text-ink/60">
                  Status
                  <select
                    value={c.status}
                    disabled={savingId === c.id}
                    onChange={(e) => updateComplaint(c.id, { status: e.target.value })}
                    className="ml-2 rounded-md border border-ink/15 px-2 py-1 text-sm"
                  >
                    {STATUS_OPTIONS.map((s) => (
                      <option key={s} value={s}>
                        {s.replace("_", " ")}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="text-xs font-medium text-ink/60">
                  Priority
                  <select
                    value={c.priority}
                    disabled={savingId === c.id}
                    onChange={(e) => updateComplaint(c.id, { priority: e.target.value })}
                    className="ml-2 rounded-md border border-ink/15 px-2 py-1 text-sm"
                  >
                    {PRIORITY_OPTIONS.map((p) => (
                      <option key={p} value={p}>
                        {p}
                      </option>
                    ))}
                  </select>
                </label>

                {savingId === c.id && (
                  <span className="text-xs text-ink/40">Saving…</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
