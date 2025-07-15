export interface InteractionTracking {
  started_at: number;
  field_interactions: Record<string, number>;
  total_fields_interacted: number;
  form_abandonment_point?: string;
  total_time_spent?: number;
}

export interface FieldInteraction {
  field: string;
  type: 'focus' | 'blur' | 'change';
  timestamp: number;
}
