/**
 * Progress Tracker API Client
 *
 * Fetch wrapper for communicating with Progress Tracker backend
 */

export interface TopicMastery {
  topic: string;
  mastery_level: number;
  interactions_count: number;
}

export interface MasteryResponse {
  student_id: string;
  overall_mastery: number;
  topic_mastery: TopicMastery[];
  struggling_topics: string[];
  next_recommended_topic: string | null;
}

export interface StruggleDetectionRequest {
  student_id: string;
  recent_queries: string[];
  recent_errors: string[];
}

export interface StruggleDetectionResponse {
  student_id: string;
  is_struggling: boolean;
  confidence: number;
  struggle_indicators: string[];
  suggested_interventions: string[];
}

/**
 * Fetch student mastery data
 */
export async function fetchMastery(studentId: string): Promise<MasteryResponse> {
  const response = await fetch(`/api/mastery?studentId=${encodeURIComponent(studentId)}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
    // No caching - always fetch fresh data
    cache: 'no-store',
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch mastery: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Update student mastery for a topic
 */
export async function updateMastery(
  studentId: string,
  topic: string,
  interactionType: 'query' | 'success' | 'error' | 'hint_request',
  success: boolean
): Promise<MasteryResponse> {
  // Call backend API route (to be created)
  const response = await fetch(`/api/mastery/${studentId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      topic,
      interaction_type: interactionType,
      success,
    }),
  });

  if (!response.ok) {
    throw new Error(`Failed to update mastery: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Fetch learning insights for a student
 */
export async function fetchInsights(studentId: string) {
  const response = await fetch(`/api/insights?studentId=${encodeURIComponent(studentId)}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
    cache: 'no-store',
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch insights: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Detect if student is struggling
 */
export async function detectStruggle(
  request: StruggleDetectionRequest
): Promise<StruggleDetectionResponse> {
  const response = await fetch('/api/struggle-detection', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Failed to detect struggle: ${response.statusText}`);
  }

  return response.json();
}
