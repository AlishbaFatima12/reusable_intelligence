/**
 * Mastery API Route
 *
 * Fetches student mastery data from Progress Tracker Agent (port 8006)
 *
 * GET /api/mastery?studentId=<id>
 */

import { NextRequest, NextResponse } from 'next/server';

// Progress Tracker backend URL
const PROGRESS_TRACKER_URL = process.env.PROGRESS_TRACKER_URL || 'http://localhost:8006';

export async function GET(request: NextRequest) {
  try {
    // Get student ID from query params (default to demo student)
    const { searchParams } = new URL(request.url);
    const studentId = searchParams.get('studentId') || 'demo-student-001';

    // Fetch mastery data from Progress Tracker
    const response = await fetch(
      `${PROGRESS_TRACKER_URL}/api/v1/mastery/${studentId}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        // No caching - always fetch fresh data
        cache: 'no-store',
      }
    );

    if (!response.ok) {
      // If student not found, return default initial mastery
      if (response.status === 404) {
        return NextResponse.json({
          student_id: studentId,
          overall_mastery: 0.0,
          topic_mastery: [
            { topic: 'variables-and-data-types', mastery_level: 0.0, interactions_count: 0 },
            { topic: 'control-flow', mastery_level: 0.0, interactions_count: 0 },
            { topic: 'functions', mastery_level: 0.0, interactions_count: 0 },
            { topic: 'data-structures', mastery_level: 0.0, interactions_count: 0 },
            { topic: 'object-oriented-programming', mastery_level: 0.0, interactions_count: 0 },
            { topic: 'file-io-and-exceptions', mastery_level: 0.0, interactions_count: 0 },
            { topic: 'modules-and-packages', mastery_level: 0.0, interactions_count: 0 },
          ],
          struggling_topics: [],
          next_recommended_topic: 'variables-and-data-types',
        });
      }

      throw new Error(`Progress Tracker returned ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

    // Transform backend response to frontend format
    return NextResponse.json({
      student_id: data.student_id,
      overall_mastery: data.overall_mastery,
      topic_mastery: data.topic_mastery,
      struggling_topics: data.struggling_topics || [],
      next_recommended_topic: data.next_recommended_topic,
    });

  } catch (error) {
    console.error('Error fetching mastery data:', error);

    // Return error response
    return NextResponse.json(
      {
        error: 'Failed to fetch mastery data',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}
