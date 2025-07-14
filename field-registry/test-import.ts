// Test JSON import with TypeScript
import trackingFieldsData from './tracking.json' assert { type: 'json' };

// Or with require for CommonJS compatibility
const trackingFields = require('./tracking.json');

// Or dynamic import
const loadTrackingFields = async () => {
  const { default: data } = await import('./tracking.json', {
    assert: { type: 'json' }
  });
  return data;
};

export { trackingFieldsData, trackingFields, loadTrackingFields };
