import React, { useState } from 'react';

const ZoneFeedbackForm = ({ zoneId, onSubmit }) => {
  const [feedback, setFeedback] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!feedback.trim()) return;
    onSubmit && onSubmit(zoneId, feedback);
    setFeedback('');
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 2000);
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: 4, display: 'flex', gap: 6 }}>
      <input
        type="text"
        value={feedback}
        onChange={e => setFeedback(e.target.value)}
        placeholder="Feedback (e.g. false positive, needs rescue, etc)"
        style={{ flex: 1, fontSize: 12, padding: '4px 8px', borderRadius: 4, border: '1px solid #cbd5e1' }}
      />
      <button type="submit" style={{ fontSize: 12, padding: '4px 10px', borderRadius: 4, border: 'none', background: '#10b981', color: 'white', cursor: 'pointer' }}>Send</button>
      {submitted && <span style={{ color: '#10b981', fontSize: 12 }}>✓</span>}
    </form>
  );
};

export default ZoneFeedbackForm;
