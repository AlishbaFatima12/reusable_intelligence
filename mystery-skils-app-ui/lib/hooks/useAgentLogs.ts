/**
 * useAgentLogs Hook
 *
 * Connects to WebSocket server for real-time agent logs and events
 */

'use client';

import { useState, useEffect, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';

export interface AgentLog {
  id: string;
  agent: string;
  level: 'INFO' | 'WARN' | 'ERROR' | 'SUCCESS';
  message: string;
  timestamp: string;
  data?: any;
}

export interface MasteryUpdate {
  student_id: string;
  topic: string;
  old_mastery: number;
  new_mastery: number;
  struggling_topics: string[];
  timestamp: string;
}

export interface StruggleAlert {
  student_id: string;
  confidence: number;
  indicators: string[];
  interventions: string[];
  timestamp: string;
}

interface AgentLogsState {
  logs: AgentLog[];
  masteryUpdates: MasteryUpdate[];
  struggleAlerts: StruggleAlert[];
  isConnected: boolean;
}

/**
 * Hook to connect to WebSocket server and receive real-time events
 *
 * @param socketUrl - WebSocket server URL (defaults to localhost:4001)
 * @param maxLogs - Maximum number of logs to keep in memory (default: 100)
 */
export function useAgentLogs(
  socketUrl: string = 'http://localhost:4001',
  maxLogs: number = 100
) {
  const [state, setState] = useState<AgentLogsState>({
    logs: [],
    masteryUpdates: [],
    struggleAlerts: [],
    isConnected: false,
  });

  const [socket, setSocket] = useState<Socket | null>(null);

  useEffect(() => {
    // Create Socket.io client
    const newSocket = io(socketUrl, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
    });

    // Connection events
    newSocket.on('connect', () => {
      console.log('WebSocket connected');
      setState(prev => ({ ...prev, isConnected: true }));
    });

    newSocket.on('disconnect', () => {
      console.log('WebSocket disconnected');
      setState(prev => ({ ...prev, isConnected: false }));
    });

    newSocket.on('connection_status', (data: any) => {
      console.log('Connection status:', data);
    });

    // Agent log events
    newSocket.on('agent-log', (data: any) => {
      const newLog: AgentLog = {
        id: `${Date.now()}-${Math.random()}`,
        agent: data.agent || 'UNKNOWN',
        level: data.level || 'INFO',
        message: data.message || data.data?.message || 'No message',
        timestamp: data.timestamp || new Date().toISOString(),
        data: data.data,
      };

      setState(prev => ({
        ...prev,
        logs: [newLog, ...prev.logs].slice(0, maxLogs),
      }));
    });

    // Mastery update events
    newSocket.on('mastery-update', (data: MasteryUpdate) => {
      console.log('Mastery update received:', data);

      setState(prev => ({
        ...prev,
        masteryUpdates: [data, ...prev.masteryUpdates].slice(0, 20),
      }));
    });

    // Student struggle alert events
    newSocket.on('student-struggle', (data: StruggleAlert) => {
      console.log('Struggle alert received:', data);

      setState(prev => ({
        ...prev,
        struggleAlerts: [data, ...prev.struggleAlerts].slice(0, 10),
      }));
    });

    // Routing decision events
    newSocket.on('routing-decision', (data: any) => {
      const routingLog: AgentLog = {
        id: `routing-${Date.now()}`,
        agent: 'TRIAGE',
        level: 'INFO',
        message: `Routed to ${data.routed_to_agent} (intent: ${data.detected_intent})`,
        timestamp: data.timestamp || new Date().toISOString(),
        data,
      };

      setState(prev => ({
        ...prev,
        logs: [routingLog, ...prev.logs].slice(0, maxLogs),
      }));
    });

    // Agent response events
    newSocket.on('agent-response', (data: any) => {
      const responseLog: AgentLog = {
        id: `response-${Date.now()}`,
        agent: data.agent || 'AGENT',
        level: 'SUCCESS',
        message: `Response generated for query ${data.query_id}`,
        timestamp: data.timestamp || new Date().toISOString(),
        data,
      };

      setState(prev => ({
        ...prev,
        logs: [responseLog, ...prev.logs].slice(0, maxLogs),
      }));
    });

    setSocket(newSocket);

    // Cleanup on unmount
    return () => {
      newSocket.disconnect();
    };
  }, [socketUrl, maxLogs]);

  // Clear logs function
  const clearLogs = useCallback(() => {
    setState(prev => ({ ...prev, logs: [] }));
  }, []);

  // Manual reconnect
  const reconnect = useCallback(() => {
    if (socket) {
      socket.disconnect();
      socket.connect();
    }
  }, [socket]);

  return {
    ...state,
    clearLogs,
    reconnect,
  };
}
