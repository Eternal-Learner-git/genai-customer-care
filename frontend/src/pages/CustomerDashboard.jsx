import React, { useEffect, useState } from "react";
import apiClient from "../api/client";
import ComplaintCard from "../components/ComplaintCard";

export default function CustomerDashboard() {
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [subject, setSubject] = useState("");
  const [description, setDescription] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function loadComplaints() {
    setLoading(true);
    try {
      const res = await apiClient.get("/complaints/me");
      setComplaints(res.data);
    } catch {
      setError("Couldn't load your complaints. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadComplaints();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await apiClient.post("/complaints", { subject, description });
      setSubject("");
      setDescription("");
      await loadComplaints();
      // Category/sentiment/priority/suggested_response are filled in by a background
      // task (NLP + RAG services), which takes a few seconds - refresh once more
      // after a short delay so they show up without the user having to do anything.
      setTimeout(loadComplaints, 6000);
    } catch {
      setError("Couldn't submit your complaint. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="font-display text-3xl text-teal-700">File a complaint</h1>
      <p className="mt-1 text-sm text-ink/60">
        Tell us what happened. We'll route it to the right team.
      </p>

      <form
        onSubmit={handleSubmit}
        className="mt-6 space-y-4 rounded-lg border border-ink/10 bg-white p-6"
      >
        <div>
          <label className="block text-sm font-medium text-ink/80">Subject</label>
          <input
            type="text"
            required
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            placeholder="Short summary of the issue"
            className="mt-1 w-full rounded-md border border-ink/15 px-3 py-2 focus:border-teal-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-ink/80">Description</label>
          <textarea
            required
            rows={4}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="What happened, and when?"
            className="mt-1 w-full rounded-md border border-ink/15 px-3 py-2 focus:border-teal-500"
          />
        </div>

        {error && <p className="text-sm text-coral-500">{error}</p>}

        <button
          type="submit"
          disabled={submitting}
          className="rounded-md bg-teal-500 px-5 py-2 font-medium text-white hover:bg-teal-600 disabled:opacity-60"
        >
          {submitting ? "Submitting…" : "Submit complaint"}
        </button>
      </form>

      <div className="mt-10 flex items-center justify-between">
        <h2 className="font-display text-2xl text-teal-700">Your complaints</h2>
        <button
          onClick={loadComplaints}
          className="text-sm text-teal-600 hover:underline"
        >
          Refresh
        </button>
      </div>

      <p className="mt-1 text-xs text-ink/40">
        Category, sentiment, and a suggested response are added automatically a few
        seconds after you submit — refresh if you don't see them yet.
      </p>

      {loading ? (
        <p className="mt-4 text-sm text-ink/50">Loading…</p>
      ) : complaints.length === 0 ? (
        <p className="mt-4 text-sm text-ink/50">
          You haven't filed any complaints yet — the one you submit above will show up here.
        </p>
      ) : (
        <div className="mt-4 space-y-4">
          {complaints.map((c) => (
            <ComplaintCard key={c.id} complaint={c} />
          ))}
        </div>
      )}
    </div>
  );
}
