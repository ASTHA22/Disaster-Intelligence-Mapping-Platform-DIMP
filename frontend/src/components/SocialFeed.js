import React from 'react';
import { MessageSquare, MapPin, Clock, CheckCircle } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import './SocialFeed.css';

const SocialFeed = ({ posts }) => {
  const getUrgencyClass = (urgency) => {
    return `post-urgency urgency-${urgency}`;
  };

  return (
    <div className="social-feed">
      <div className="feed-header">
        <MessageSquare size={20} />
        <h3>Social Media Intelligence</h3>
      </div>

      <div className="feed-list">
        {posts.map((post, idx) => (
          <div key={post.id || idx} className="feed-post">
            <div className="post-header">
              <span className={`post-urgency urgency-${post.urgency || 'medium'}`}>{post.urgency || 'medium'}</span>
              {post.verified && <span className="verified-badge">Verified</span>}
            </div>
            <div className="post-content">
              <p>{post.text}</p>
              {post.location && (
                <div className="post-location" style={{ color: '#2563eb', fontWeight: 600, fontSize: 13, marginTop: 4 }}>
                  📍 {post.location}
                </div>
              )}
            </div>
            <div className="post-meta">
              <span className="meta-item">{post.source ? `Source: ${post.source}` : ''}</span>
              <span className="meta-item">{post.timestamp ? new Date(post.timestamp).toLocaleString() : ''}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SocialFeed;
