'use client'

import { useState, useEffect } from 'react'
import { MasterySphere } from '@/components/ui/MasterySphere'
import { HackerTerminal } from '@/components/ui/HackerTerminal'
import { TeacherHUD } from '@/components/ui/TeacherHUD'
import { useMasteryState } from '@/lib/hooks/useMasteryState'
import { useAgentLogs } from '@/lib/hooks/useAgentLogs'

export default function MysterySkillsPage() {
  const { masteryLevels, updateMastery } = useMasteryState()
  const { logs, struggling Students } = useAgentLogs()

  return (
    <div className="relative w-full h-screen bg-black overflow-hidden">
      {/* Background Grid Effect */}
      <div className="absolute inset-0 bg-grid-pattern opacity-20" />

      {/* Main Content Grid */}
      <div className="relative z-10 grid grid-cols-12 gap-4 h-full p-6">

        {/* Left Column - Teacher HUD */}
        <div className="col-span-3 flex flex-col gap-4">
          <TeacherHUD strugglingStudents={strugglingStudents} />
        </div>

        {/* Center Column - 3D Mastery Sphere */}
        <div className="col-span-6 flex items-center justify-center">
          <MasterySphere masteryLevels={masteryLevels} />
        </div>

        {/* Right Column - Hacker Terminal */}
        <div className="col-span-3 flex flex-col gap-4">
          <HackerTerminal logs={logs} />
        </div>
      </div>

      {/* Title Overlay */}
      <div className="absolute top-8 left-1/2 transform -translate-x-1/2 z-20">
        <h1 className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 animate-pulse">
          MYSTERY SKILLS
        </h1>
        <p className="text-center text-gray-400 mt-2 text-sm tracking-widest">
          REAL-TIME LEARNING MASTERY VISUALIZATION
        </p>
      </div>
    </div>
  )
}
