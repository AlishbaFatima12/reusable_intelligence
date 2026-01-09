'use client'

import { useState, useEffect } from 'react'
import DottedGlowBackground from '@/components/DottedGlowBackground'
import ArtifactCard from '@/components/ArtifactCard'
import SideDrawer from '@/components/SideDrawer'
import { Artifact } from '@/types'
import { useMasteryState } from '@/lib/hooks/useMasteryState'
import { useAgentLogs } from '@/lib/hooks/useAgentLogs'

export default function MysterySkillsPage() {
  const [artifacts, setArtifacts] = useState<Artifact[]>([])
  const [focusedArtifactId, setFocusedArtifactId] = useState<string | null>(null)
  const [isDrawerOpen, setIsDrawerOpen] = useState(false)

  // Fetch data from LearnFlow backend via hooks
  const { topicMastery, overallMastery, strugglingTopics, isLoading: masteryLoading } = useMasteryState('demo-student-001', 5000)
  const { logs, masteryUpdates, struggleAlerts, isConnected } = useAgentLogs('http://localhost:4001', 100)

  // Convert mastery data to artifacts
  useEffect(() => {
    if (topicMastery.length > 0) {
      const masteryArtifacts: Artifact[] = topicMastery.map((topic, idx) => {
        const masteryPercent = Math.round(topic.mastery_level * 100)
        const colorClass = masteryPercent >= 66 ? 'blue' : masteryPercent >= 33 ? 'green' : masteryPercent > 0 ? 'orange' : 'red'
        const gradients = {
          blue: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
          green: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
          orange: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
          red: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)'
        }

        return {
          id: `mastery-${topic.topic}`,
          styleName: `${topic.topic.replace(/-/g, ' ').toUpperCase()}`,
          html: `
            <!DOCTYPE html>
            <html>
            <head>
              <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
                  background: ${gradients[colorClass as keyof typeof gradients]};
                  color: white;
                  display: flex;
                  flex-direction: column;
                  justify-content: center;
                  align-items: center;
                  min-height: 100%;
                  padding: 24px;
                }
                .container {
                  text-align: center;
                  width: 100%;
                }
                h2 {
                  font-size: 20px;
                  font-weight: 600;
                  margin-bottom: 20px;
                  text-transform: capitalize;
                  letter-spacing: 0.5px;
                }
                .mastery-value {
                  font-size: 64px;
                  font-weight: 900;
                  margin-bottom: 8px;
                  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
                }
                .label {
                  font-size: 14px;
                  opacity: 0.9;
                  text-transform: uppercase;
                  letter-spacing: 1px;
                }
                .interactions {
                  margin-top: 16px;
                  font-size: 12px;
                  opacity: 0.8;
                }
              </style>
            </head>
            <body>
              <div class="container">
                <h2>${topic.topic.replace(/-/g, ' ')}</h2>
                <div class="mastery-value">${masteryPercent}%</div>
                <div class="label">Mastery Level</div>
                <div class="interactions">${topic.interactions_count} interactions</div>
              </div>
            </body>
            </html>
          `,
          status: 'complete' as const
        }
      })

      // Add overall mastery card
      const overallPercent = Math.round(overallMastery * 100)
      const overallArtifact: Artifact = {
        id: 'mastery-overall',
        styleName: 'OVERALL MASTERY',
        html: `
          <!DOCTYPE html>
          <html>
          <head>
            <style>
              * { margin: 0; padding: 0; box-sizing: border-box; }
              body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100%;
                padding: 24px;
              }
              .container {
                text-align: center;
                width: 100%;
              }
              h1 {
                font-size: 24px;
                font-weight: 700;
                margin-bottom: 24px;
                text-transform: uppercase;
                letter-spacing: 2px;
              }
              .mastery-value {
                font-size: 80px;
                font-weight: 900;
                margin-bottom: 12px;
                text-shadow: 0 4px 12px rgba(0,0,0,0.3);
              }
              .label {
                font-size: 16px;
                opacity: 0.95;
                text-transform: uppercase;
                letter-spacing: 1.5px;
              }
            </style>
          </head>
          <body>
            <div class="container">
              <h1>Overall Progress</h1>
              <div class="mastery-value">${overallPercent}%</div>
              <div class="label">Total Mastery</div>
            </div>
          </body>
          </html>
        `,
        status: 'complete' as const
      }

      setArtifacts([overallArtifact, ...masteryArtifacts])
    }
  }, [topicMastery, overallMastery])

  return (
    <div className="relative w-full min-h-screen bg-black text-white overflow-hidden">
      <DottedGlowBackground
        className="fixed inset-0"
        gap={16}
        radius={2.5}
        color="rgba(139, 92, 246, 0.15)"
        glowColor="rgba(139, 92, 246, 0.9)"
      />

      <div className="relative z-10 container mx-auto px-6 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-purple-500 to-pink-600 mb-4">
            MYSTERY SKILLS
          </h1>
          <p className="text-2xl text-gray-300 tracking-wider">
            The Learning Revolution
          </p>
          <p className="text-sm text-gray-400 mt-2 italic">
            by Syeda Alishba Fatima
          </p>

          {/* Connection Status */}
          <div className="mt-6 flex justify-center items-center gap-4">
            <div className="flex items-center gap-2">
              <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'} ${isConnected ? 'animate-pulse' : ''}`} />
              <span className="text-sm text-gray-400">
                WebSocket {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <div className={`w-3 h-3 rounded-full ${!masteryLoading ? 'bg-green-500' : 'bg-yellow-500'} ${!masteryLoading ? 'animate-pulse' : ''}`} />
              <span className="text-sm text-gray-400">
                Backend {!masteryLoading ? 'Ready' : 'Loading...'}
              </span>
            </div>
          </div>
        </div>

        {/* Struggling Topics Alert */}
        {strugglingTopics.length > 0 && (
          <div className="mb-8 p-4 bg-red-900/30 border border-red-500/50 rounded-lg">
            <h3 className="text-red-400 font-semibold mb-2">Struggling Topics Detected</h3>
            <div className="flex flex-wrap gap-2">
              {strugglingTopics.map(topic => (
                <span key={topic} className="px-3 py-1 bg-red-500/20 border border-red-500/40 rounded-full text-sm text-red-300">
                  {topic.replace(/-/g, ' ')}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Artifacts Grid */}
        {artifacts.length === 0 ? (
          <div className="text-center py-20">
            <div className="text-4xl font-bold text-gray-500 mb-4 animate-pulse">
              Loading Mastery Data...
            </div>
            <p className="text-gray-600">Connecting to LearnFlow backend agents</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {artifacts.map(artifact => (
              <ArtifactCard
                key={artifact.id}
                artifact={artifact}
                isFocused={focusedArtifactId === artifact.id}
                onClick={() => setFocusedArtifactId(artifact.id)}
              />
            ))}
          </div>
        )}

        {/* Agent Logs Toggle Button */}
        <button
          onClick={() => setIsDrawerOpen(!isDrawerOpen)}
          className="fixed bottom-8 right-8 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-6 py-3 rounded-full shadow-lg transition-all transform hover:scale-105 flex items-center gap-2"
        >
          <span className="relative flex h-3 w-3">
            {logs.length > 0 && (
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
            )}
            <span className="relative inline-flex rounded-full h-3 w-3 bg-white"></span>
          </span>
          {isDrawerOpen ? 'Close Logs' : `View Logs (${logs.length})`}
        </button>
      </div>

      <SideDrawer
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
        title="Agent Logs"
      >
        <div className="space-y-4">
          {/* Mastery Updates Section */}
          {masteryUpdates.length > 0 && (
            <div>
              <h3 className="text-purple-400 font-semibold mb-2 text-sm uppercase tracking-wider">
                Recent Mastery Updates
              </h3>
              <div className="space-y-2">
                {masteryUpdates.slice(0, 5).map((update, idx) => (
                  <div key={idx} className="p-3 bg-purple-900/20 border border-purple-500/30 rounded">
                    <div className="text-sm font-medium text-purple-300">
                      {update.topic.replace(/-/g, ' ')}
                    </div>
                    <div className="text-xs text-gray-400 mt-1">
                      {Math.round(update.old_mastery * 100)}% → {Math.round(update.new_mastery * 100)}%
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Struggle Alerts Section */}
          {struggleAlerts.length > 0 && (
            <div>
              <h3 className="text-red-400 font-semibold mb-2 text-sm uppercase tracking-wider">
                Struggle Alerts
              </h3>
              <div className="space-y-2">
                {struggleAlerts.slice(0, 3).map((alert, idx) => (
                  <div key={idx} className="p-3 bg-red-900/20 border border-red-500/30 rounded">
                    <div className="text-sm font-medium text-red-300">
                      Confidence: {Math.round(alert.confidence * 100)}%
                    </div>
                    <div className="text-xs text-gray-400 mt-1">
                      {alert.indicators.join(', ')}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Agent Logs Section */}
          <div>
            <h3 className="text-cyan-400 font-semibold mb-2 text-sm uppercase tracking-wider">
              Agent Activity
            </h3>
            <div className="space-y-2 max-h-[400px] overflow-y-auto scrollbar-thin scrollbar-thumb-cyan-500/50 scrollbar-track-transparent">
              {logs.length === 0 ? (
                <div className="text-gray-500 text-sm text-center py-4">
                  No logs yet. Waiting for agent activity...
                </div>
              ) : (
                logs.map((log) => (
                  <div key={log.id} className="p-3 bg-gray-900/50 border border-gray-700 rounded">
                    <div className="flex items-center justify-between mb-1">
                      <span className={`text-xs font-semibold px-2 py-1 rounded ${
                        log.level === 'ERROR' ? 'bg-red-500/20 text-red-400' :
                        log.level === 'WARN' ? 'bg-yellow-500/20 text-yellow-400' :
                        log.level === 'SUCCESS' ? 'bg-green-500/20 text-green-400' :
                        'bg-blue-500/20 text-blue-400'
                      }`}>
                        {log.agent}
                      </span>
                      <span className="text-xs text-gray-500">
                        {new Date(log.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                    <div className="text-sm text-gray-300">
                      {log.message}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </SideDrawer>
    </div>
  )
}
