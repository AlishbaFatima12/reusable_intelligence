'use client'

import { motion } from 'framer-motion'

export interface StrugglingStudent {
  id: string
  name: string
  failedRuns: number
  currentTopic: string
  lastActivity: string
  struggling: boolean
}

interface Props {
  strugglingStudents: StrugglingStudent[]
}

export function TeacherHUD({ strugglingStudents }: Props) {
  const activeStrugglers = strugglingStudents.filter(s => s.struggling)

  return (
    <div className="h-full flex flex-col gap-4">
      {/* Header Card */}
      <motion.div
        className="relative bg-gradient-to-br from-purple-900/40 to-pink-900/40 backdrop-blur-sm border border-purple-500/30 rounded-lg p-4"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">
            TEACHER HUD
          </h2>
          {activeStrugglers.length > 0 && (
            <motion.div
              className="px-3 py-1 bg-red-500/20 border border-red-500 rounded-full"
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 1, repeat: Infinity }}
            >
              <span className="text-red-400 text-sm font-bold">
                {activeStrugglers.length} ALERT{activeStrugglers.length !== 1 ? 'S' : ''}
              </span>
            </motion.div>
          )}
        </div>

        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <div className="text-gray-400">Total Students</div>
            <div className="text-2xl font-bold text-white">{strugglingStudents.length}</div>
          </div>
          <div>
            <div className="text-gray-400">Struggling</div>
            <div className="text-2xl font-bold text-red-400">{activeStrugglers.length}</div>
          </div>
        </div>
      </motion.div>

      {/* Student List */}
      <div className="flex-1 space-y-2 overflow-y-auto scrollbar-thin scrollbar-thumb-purple-500/50 scrollbar-track-transparent">
        {strugglingStudents.length === 0 ? (
          <div className="text-center text-gray-600 italic py-8">
            No active students
          </div>
        ) : (
          strugglingStudents.map((student, index) => (
            <motion.div
              key={student.id}
              className={`relative p-4 rounded-lg border backdrop-blur-sm ${
                student.struggling
                  ? 'bg-red-900/20 border-red-500/50'
                  : 'bg-gray-900/40 border-gray-700/30'
              }`}
              initial={{ opacity: 0, x: -20 }}
              animate={{
                opacity: 1,
                x: 0,
                scale: student.struggling ? [1, 1.02, 1] : 1
              }}
              transition={{
                duration: 0.3,
                delay: index * 0.1,
                scale: { duration: 2, repeat: student.struggling ? Infinity : 0 }
              }}
            >
              {/* Struggle Alert Badge */}
              {student.struggling && (
                <motion.div
                  className="absolute -top-2 -right-2 w-8 h-8 bg-red-500 rounded-full flex items-center justify-center border-2 border-black"
                  animate={{
                    rotate: [0, 10, -10, 0],
                    scale: [1, 1.2, 1]
                  }}
                  transition={{ duration: 1, repeat: Infinity }}
                >
                  <span className="text-white text-xs font-bold">!</span>
                </motion.div>
              )}

              <div className="flex items-start justify-between mb-2">
                <div>
                  <div className={`font-bold ${student.struggling ? 'text-red-400' : 'text-white'}`}>
                    {student.name}
                  </div>
                  <div className="text-xs text-gray-400">{student.id}</div>
                </div>
                <div className={`text-right text-xs ${student.struggling ? 'text-red-400' : 'text-gray-400'}`}>
                  {student.lastActivity}
                </div>
              </div>

              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">Topic:</span>
                  <span className="text-cyan-400 font-mono">{student.currentTopic}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Failed Runs:</span>
                  <div className="flex items-center gap-2">
                    <span className={`font-bold ${
                      student.failedRuns >= 5 ? 'text-red-400' :
                      student.failedRuns >= 3 ? 'text-yellow-400' :
                      'text-green-400'
                    }`}>
                      {student.failedRuns}
                    </span>
                    {student.failedRuns >= 5 && (
                      <span className="text-xs px-2 py-0.5 bg-red-500/20 border border-red-500 rounded text-red-400">
                        NEEDS HELP
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="mt-3 h-1 bg-gray-800 rounded-full overflow-hidden">
                <motion.div
                  className={`h-full ${
                    student.struggling ? 'bg-red-500' : 'bg-green-500'
                  }`}
                  initial={{ width: 0 }}
                  animate={{ width: `${Math.max(0, 100 - student.failedRuns * 10)}%` }}
                  transition={{ duration: 0.5 }}
                />
              </div>
            </motion.div>
          ))
        )}
      </div>
    </div>
  )
}
