'use client';

import { useMasteryState, transformToRingData } from '@/lib/hooks/useMasteryState';
import { useAgentLogs } from '@/lib/hooks/useAgentLogs';

export default function Home() {
  // Fetch student mastery data
  const mastery = useMasteryState('demo-student-001', 5000);

  // Connect to WebSocket for real-time logs
  const { logs, masteryUpdates, struggleAlerts, isConnected } = useAgentLogs(
    'http://localhost:4001',
    100
  );

  // Transform mastery to ring data
  const ringData = transformToRingData(mastery.topicMastery);

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 glow-text text-hacker-green">
          Mystery Skills - LearnFlow Platform
        </h1>

        {/* Connection Status */}
        <div className="mb-6">
          <div className="flex items-center gap-2">
            <div
              className={`w-3 h-3 rounded-full ${
                isConnected ? 'bg-green-500' : 'bg-red-500'
              } animate-pulse`}
            />
            <span className="text-sm">
              {isConnected ? 'WebSocket Connected' : 'WebSocket Disconnected'}
            </span>
          </div>
        </div>

        {/* Mastery Overview */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Mastery Stats */}
          <div className="border border-hacker-green/30 rounded-lg p-6 bg-black/50">
            <h2 className="text-2xl font-bold mb-4 text-hacker-cyan">Student Mastery</h2>

            {mastery.isLoading ? (
              <div className="text-gray-400">Loading mastery data...</div>
            ) : mastery.error ? (
              <div className="text-red-500">Error: {mastery.error}</div>
            ) : (
              <div>
                <div className="mb-4">
                  <div className="text-sm text-gray-400">Overall Mastery</div>
                  <div className="text-3xl font-bold text-hacker-green">
                    {(mastery.overallMastery * 100).toFixed(1)}%
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="text-sm text-gray-400 mb-2">Topics:</div>
                  {ringData.map((ring) => (
                    <div key={ring.topic} className="flex justify-between items-center">
                      <span className="text-sm">{ring.topic}</span>
                      <div className="flex items-center gap-2">
                        <div
                          className="w-4 h-4 rounded-full"
                          style={{ backgroundColor: ring.color }}
                        />
                        <span className="text-sm">{(ring.masteryLevel * 100).toFixed(0)}%</span>
                      </div>
                    </div>
                  ))}
                </div>

                {mastery.strugglingTopics.length > 0 && (
                  <div className="mt-4 p-3 border border-red-500/50 rounded bg-red-500/10">
                    <div className="text-sm text-red-400 font-bold">Struggling Topics:</div>
                    <div className="text-sm text-red-300">
                      {mastery.strugglingTopics.join(', ')}
                    </div>
                  </div>
                )}

                {mastery.nextRecommendedTopic && (
                  <div className="mt-4 p-3 border border-blue-500/50 rounded bg-blue-500/10">
                    <div className="text-sm text-blue-400 font-bold">Next Topic:</div>
                    <div className="text-sm text-blue-300">{mastery.nextRecommendedTopic}</div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Recent Logs */}
          <div className="border border-hacker-green/30 rounded-lg p-6 bg-black/50">
            <h2 className="text-2xl font-bold mb-4 text-hacker-cyan">Agent Logs</h2>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {logs.length === 0 ? (
                <div className="text-gray-400 text-sm">No logs yet...</div>
              ) : (
                logs.slice(0, 10).map((log) => (
                  <div key={log.id} className="text-xs font-mono border-l-2 border-hacker-green/50 pl-2">
                    <div className="flex items-center gap-2">
                      <span className={`font-bold ${
                        log.level === 'ERROR' ? 'text-red-500' :
                        log.level === 'WARN' ? 'text-yellow-500' :
                        log.level === 'SUCCESS' ? 'text-green-500' :
                        'text-hacker-cyan'
                      }`}>
                        [{log.level}]
                      </span>
                      <span className="text-hacker-green">{log.agent}</span>
                      <span className="text-gray-400">{log.message}</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Real-time Updates */}
        {(masteryUpdates.length > 0 || struggleAlerts.length > 0) && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Mastery Updates */}
            {masteryUpdates.length > 0 && (
              <div className="border border-blue-500/30 rounded-lg p-6 bg-black/50">
                <h2 className="text-xl font-bold mb-4 text-blue-400">Mastery Updates</h2>
                <div className="space-y-2">
                  {masteryUpdates.slice(0, 5).map((update, i) => (
                    <div key={i} className="text-sm border-l-2 border-blue-500/50 pl-2">
                      <div className="text-blue-300">{update.topic}</div>
                      <div className="text-gray-400">
                        {(update.old_mastery * 100).toFixed(0)}% → {(update.new_mastery * 100).toFixed(0)}%
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Struggle Alerts */}
            {struggleAlerts.length > 0 && (
              <div className="border border-red-500/30 rounded-lg p-6 bg-black/50 animate-pulse-slow">
                <h2 className="text-xl font-bold mb-4 text-red-400">⚠️ Struggle Alerts</h2>
                <div className="space-y-2">
                  {struggleAlerts.slice(0, 3).map((alert, i) => (
                    <div key={i} className="text-sm border-l-2 border-red-500/50 pl-2">
                      <div className="text-red-300 font-bold">
                        Student: {alert.student_id} (Confidence: {(alert.confidence * 100).toFixed(0)}%)
                      </div>
                      <div className="text-gray-400 text-xs">
                        Indicators: {alert.indicators.join(', ')}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Instructions */}
        <div className="mt-8 p-6 border border-gray-700 rounded-lg bg-black/30">
          <h2 className="text-xl font-bold mb-2">🚀 Getting Started</h2>
          <div className="text-sm text-gray-400 space-y-2">
            <p>This is the Mystery Skills UI connected to the LearnFlow backend.</p>
            <p><strong>Backend agents running?</strong> Start them first:</p>
            <code className="block bg-black/50 p-2 rounded mt-2">
              cd backend/agents/triage && uvicorn main:app --port 8001 --reload<br />
              cd backend/agents/concepts && uvicorn main:app --port 8002 --reload<br />
              cd backend/agents/progress && uvicorn main:app --port 8006 --reload<br />
              cd backend/websocket-bridge && python main.py
            </code>
            <p className="mt-2"><strong>Then:</strong> npm run dev (port 4000)</p>
          </div>
        </div>
      </div>
    </div>
  );
}
