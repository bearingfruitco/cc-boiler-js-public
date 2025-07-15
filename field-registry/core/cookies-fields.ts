export const cookiesFields = {
  tracking: ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'],
  device: ['device_id', 'browser', 'os', 'screen_resolution'],
  geographic: ['ip_address', 'country', 'state', 'city'],
  journey: ['referrer', 'landing_page', 'exit_page']
};

export const trackingFields = cookiesFields.tracking;
export const deviceFields = cookiesFields.device;
export const geographicFields = cookiesFields.geographic;
export const journeyFields = cookiesFields.journey;
