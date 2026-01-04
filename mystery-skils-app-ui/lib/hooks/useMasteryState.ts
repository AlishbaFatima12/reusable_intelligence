/**
 * useMasteryState Hook
 *
 * Fetches and manages student mastery data from Progress Tracker backend
 */

'use client';

import { useState, useEffect } from 'react';
import { fetchMastery, type MasteryResponse, type TopicMastery } from '@/lib/api/progressClient';

interface MasteryState {
  studentId: string;
  overallMastery: number;
  topicMastery: TopicMastery[];
  strugglingTopics: string[];
  nextRecommendedTopic: string | null;
  isLoading: boolean;
  error: string | null;
}

/**
 * Hook to fetch and track student mastery levels
 *
 * @param studentId - Student identifier (defaults to demo student)
 * @param refreshInterval - Auto-refresh interval in ms (0 = no auto-refresh)
 */
export function useMasteryState(
  studentId: string = 'demo-student-001',
  refreshInterval: number = 5000 // Refresh every 5 seconds
) {
  const [state, setState] = useState<MasteryState>({
    studentId,
    overallMastery: 0,
    topicMastery: [],
    strugglingTopics: [],
    nextRecommendedTopic: null,
    isLoading: true,
    error: null,
  });

  // Fetch mastery data
  const fetchData = async () => {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));

      const data = await fetchMastery(studentId);

      setState({
        studentId: data.student_id,
        overallMastery: data.overall_mastery,
        topicMastery: data.topic_mastery,
        strugglingTopics: data.struggling_topics,
        nextRecommendedTopic: data.next_recommended_topic,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      console.error('Error fetching mastery data:', error);
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to fetch mastery data',
      }));
    }
  };

  // Initial fetch
  useEffect(() => {
    fetchData();
  }, [studentId]);

  // Auto-refresh
  useEffect(() => {
    if (refreshInterval <= 0) return;

    const interval = setInterval(fetchData, refreshInterval);
    return () => clearInterval(interval);
  }, [studentId, refreshInterval]);

  // Manual refresh function
  const refresh = () => {
    fetchData();
  };

  return {
    ...state,
    refresh,
  };
}

/**
 * Transform topic mastery to ring data for 3D sphere
 *
 * Maps 7 Python curriculum topics to ring colors based on mastery level
 */
export function transformToRingData(topicMastery: TopicMastery[]) {
  // Topic order for rings (inner to outer)
  const topicOrder = [
    'variables-and-data-types',
    'control-flow',
    'functions',
    'data-structures',
    'object-oriented-programming',
    'file-io-and-exceptions',
    'modules-and-packages',
  ];

  // Color mapping based on mastery level
  const getColor = (masteryLevel: number): string => {
    if (masteryLevel >= 0.66) return '#3b82f6'; // Blue (high mastery)
    if (masteryLevel >= 0.33) return '#10b981'; // Green (medium mastery)
    if (masteryLevel > 0) return '#f59e0b'; // Orange (low mastery)
    return '#ef4444'; // Red (no mastery)
  };

  // Create ring data
  return topicOrder.map(topic => {
    const mastery = topicMastery.find(tm => tm.topic === topic);
    const masteryLevel = mastery?.mastery_level ?? 0;

    return {
      topic,
      masteryLevel,
      color: getColor(masteryLevel),
      interactions: mastery?.interactions_count ?? 0,
    };
  });
}
