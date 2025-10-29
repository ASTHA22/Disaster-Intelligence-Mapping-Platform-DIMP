import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds to handle Render free tier cold start
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchDisasterData = async () => {
  try {
    const [zones, floodAreas, infrastructure, displacement, alerts, socialFeed, statistics] = 
      await Promise.all([
        api.get('/api/disaster-zones'),
        api.get('/api/flood-areas'),
        api.get('/api/infrastructure-damage'),
        api.get('/api/population-displacement'),
        api.get('/api/alerts'),
        api.get('/api/social-feed-sample'),  // Use sample data instead of live
        api.get('/api/statistics'),
      ]);

    return {
      zones: zones.data.zones || [],
      floodAreas: floodAreas.data.flood_areas || [],
      infrastructure: infrastructure.data.infrastructure || [],
      displacement: displacement.data.displacement_zones || [],
      alerts: alerts.data.alerts || [],
      socialFeed: socialFeed.data.posts || [],
      statistics: statistics.data || {},
    };
  } catch (error) {
    console.error('Error fetching disaster data:', error);
    return {
      zones: [],
      floodAreas: [],
      infrastructure: [],
      displacement: [],
      alerts: [],
      socialFeed: [],
      statistics: {},
    };
  }
};

export const analyzeImage = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await api.post('/api/analyze-image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error analyzing image:', error);
    throw error;
  }
};

export const analyzeSocialMedia = async (text, location) => {
  try {
    const response = await api.post('/api/analyze-social-media', {
      text,
      location,
      timestamp: new Date().toISOString(),
    });
    return response.data;
  } catch (error) {
    console.error('Error analyzing social media:', error);
    throw error;
  }
};

export const getHereConfig = async () => {
  try {
    const response = await api.get('/api/here-config');
    return response.data;
  } catch (error) {
    console.error('Error fetching HERE config:', error);
    return null;
  }
};

export default api;
