'use client'

import { useEffect, useRef } from 'react'
import { motion } from 'framer-motion'

export interface AgentLog {
  timestamp: string
  agent: string
  level: 'INFO' | 'WARN' | 'ERROR' | 'SUCCESS'
  message: string
}

interface Props {
  logs: AgentLog[]
}

export function HackerTerminal({ logs }: Props) {
  const terminalRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new logs arrive
  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight
    }
  }, [logs])

  const getLevelColor = (level: AgentLog['level']) => {
    switch (level) {
      case 'INFO':
        return 'text-cyan-400'
      case 'WARN':
        return 'text-yellow-400'
      case 'ERROR':
        return 'text-red-400'
      case 'SUCCESS':
        return 'text-green-400'
      default:
        return 'text-gray-400'
    }
  }

  const getAgentColor = (agent: string) => {
    const colors = [
      'text-purple-400',
      'text-blue-400',
      'text-pink-400',
      'text-indigo-400',
      'text-teal-400',
      'text-orange-400',
    ]
    const hash = agent.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
    return colors[hash % colors.length]
  }

  return (
    <motion.div
      className="relative h-full bg-black/80 backdrop-blur-sm border border-cyan-500/30 rounded-lg overflow-hidden"
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Terminal Header */}
      <div className="flex items-center justify-between px-4 py-2 bg-gradient-to-r from-cyan-900/50 to-blue-900/50 border-b border-cyan-500/30">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-red-500" />
          <div className="w-3 h-3 rounded-full bg-yellow-500" />
          <div className="w-3 h-3 rounded-full bg-green-500" />
        </div>
        <div className="text-cyan-400 text-sm font-mono font-bold tracking-widest">
          AGENT LOGS
        </div>
        <div className="text-gray-500 text-xs font-mono">
          LIVE
          <span className="inline-block ml-1 w-2 h-2 rounded-full bg-green-500 animate-pulse" />
        </div>
      </div>

      {/* Terminal Body */}
      <div
        ref={terminalRef}
        className="h-[calc(100%-3rem)] overflow-y-auto p-4 font-mono text-sm space-y-1 scrollbar-thin scrollbar-thumb-cyan-500/50 scrollbar-track-transparent"
      >
        {logs.length === 0 ? (
          <div className="text-gray-600 italic">Waiting for agent activity...</div>
        ) : (
          logs.map((log, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="flex gap-2 hover:bg-cyan-500/5 px-2 py-1 rounded"
            >
              <span className="text-gray-600 select-none">{log.timestamp}</span>
              <span className={`${getAgentColor(log.agent)} font-bold min-w-[100px]`}>
                [{log.agent}]
              </span>
              <span className={`${getLevelColor(log.level)} font-bold min-w-[60px]`}>
                {log.level}
              </span>
              <span className="text-gray-300 flex-1">{log.message}</span>
            </motion.div>
          ))
        )}
      </div>

      {/* Scanline Effect */}
      <div className="absolute inset-0 pointer-events-none bg-gradient-to-b from-transparent via-cyan-500/5 to-transparent animate-scan" />

      {/* Glow Effect */}
      <div className="absolute inset-0 pointer-events-none bg-gradient-radial from-cyan-500/10 via-transparent to-transparent" />
    </motion.div>
  )
}
