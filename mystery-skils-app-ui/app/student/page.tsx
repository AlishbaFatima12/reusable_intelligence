"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { useSession, signOut } from "@/lib/auth-client"

interface TopicMastery {
  topic_name: string
  mastery_percentage: number
  exercises_completed: number
  last_practiced: string | null
}

interface MasteryData {
  student_id: string
  overall_mastery: number
  topic_mastery: TopicMastery[]
  struggling_topics: string[]
  next_recommended_topic: string
}

export default function StudentDashboard() {
  const router = useRouter()
  const { data: session, isPending } = useSession()
  const [masteryData, setMasteryData] = useState<MasteryData | null>(null)
  const [backendStatus, setBackendStatus] = useState<"checking" | "online" | "offline">("checking")

  useEffect(() => {
    if (!isPending && !session) {
      router.push("/auth")
    }
  }, [session, isPending, router])

  useEffect(() => {
    if (session?.user) {
      checkBackendStatus()
      fetchMasteryData()
    }
  }, [session])

  const checkBackendStatus = async () => {
    try {
      const response = await fetch("http://localhost:8006/health")
      if (response.ok) {
        setBackendStatus("online")
      } else {
        setBackendStatus("offline")
      }
    } catch (error) {
      setBackendStatus("offline")
    }
  }

  const fetchMasteryData = async () => {
    try {
      const studentId = session?.user?.studentId || "demo-student-001"
      const response = await fetch(`http://localhost:8006/api/v1/mastery/${studentId}`)
      const data = await response.json()
      setMasteryData(data)
    } catch (error) {
      console.error("Failed to fetch mastery data:", error)
    }
  }

  const handleSignOut = async () => {
    await signOut()
    router.push("/auth")
  }

  const getColorForPercentage = (percent: number) => {
    if (percent >= 70) return "#39ff14" // green
    if (percent >= 40) return "#ffaa00" // amber
    return "#ff3131" // red
  }

  if (isPending || !session) {
    return (
      <div className="min-h-screen bg-black text-[#00ffcc] font-mono flex items-center justify-center">
        <div className="text-center">
          <div className="text-2xl mb-4">LOADING SYSTEM...</div>
          <div className="animate-pulse">▓▓▓▓▓▓▓▓▓▓</div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black text-[#00ffcc] font-mono p-8">
      {/* Scanlines Overlay */}
      <div className="scanlines fixed inset-0 pointer-events-none opacity-30 z-50" />

      {/* Header */}
      <div className="mb-8 border border-[#00ffcc] p-6 bg-black/75 backdrop-blur-sm">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h1 className="text-3xl font-bold mb-2">STUDENT DASHBOARD</h1>
            <div className="text-sm opacity-70">
              USER: {session.user?.email?.toUpperCase()}
            </div>
            {session.user?.studentId && (
              <div className="text-xs opacity-50">
                ID: {session.user.studentId}
              </div>
            )}
          </div>
          <button
            onClick={handleSignOut}
            className="border border-[#ff3131] px-4 py-2 hover:bg-[#ff3131] hover:text-black transition-colors"
          >
            LOGOUT
          </button>
        </div>

        <div className="flex items-center gap-2">
          <span>BACKEND STATUS:</span>
          <span
            className={`font-bold ${
              backendStatus === "online"
                ? "text-[#39ff14]"
                : backendStatus === "offline"
                ? "text-[#ff3131]"
                : "text-[#ffaa00]"
            }`}
          >
            {backendStatus.toUpperCase()}
          </span>
          {backendStatus === "online" && <span>✓</span>}
        </div>
      </div>

      {/* Mastery Overview */}
      {masteryData && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Global Mastery Card */}
          <div className="border border-[#00ffcc] p-6 bg-black/75 backdrop-blur-sm">
            <h2 className="text-xl mb-4">GLOBAL MASTERY</h2>
            <div className="text-6xl font-bold mb-4">
              {Math.round(masteryData.overall_mastery * 100)}%
            </div>
            <div className="w-full bg-gray-800 h-4">
              <div
                style={{
                  width: `${masteryData.overall_mastery * 100}%`,
                  backgroundColor: getColorForPercentage(
                    masteryData.overall_mastery * 100
                  ),
                }}
                className="h-4 transition-all duration-500"
              />
            </div>
          </div>

          {/* Next Recommended Topic */}
          <div className="border border-[#39ff14] p-6 bg-black/75 backdrop-blur-sm">
            <h2 className="text-xl mb-4 text-[#39ff14]">RECOMMENDED NEXT</h2>
            <div className="text-2xl font-bold mb-4">
              {masteryData.next_recommended_topic?.toUpperCase().replace(/-/g, " ")}
            </div>
            {masteryData.struggling_topics.length > 0 && (
              <div className="mt-4 p-3 border border-[#ff3131]">
                <div className="text-[#ff3131] font-bold mb-2">
                  ⚠ STRUGGLING TOPICS:
                </div>
                {masteryData.struggling_topics.map((topic) => (
                  <div key={topic} className="text-[#ff3131]">
                    • {topic.toUpperCase().replace(/-/g, " ")}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Topic Mastery Breakdown */}
      {masteryData && (
        <div className="border border-[#00ffcc] p-6 bg-black/75 backdrop-blur-sm">
          <h2 className="text-xl mb-6">TOPIC MASTERY BREAKDOWN</h2>
          <div className="space-y-6">
            {masteryData.topic_mastery.map((topic) => {
              const percent = Math.round(topic.mastery_percentage)
              const color = getColorForPercentage(percent)

              return (
                <div key={topic.topic_name} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-lg">
                      {topic.topic_name.toUpperCase().replace(/-/g, " ")}
                    </span>
                    <span style={{ color }} className="font-bold text-xl">
                      {percent}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-800 h-3">
                    <div
                      style={{ width: `${percent}%`, backgroundColor: color }}
                      className="h-3 transition-all duration-500"
                    />
                  </div>
                  <div className="text-xs opacity-50">
                    EXERCISES COMPLETED: {topic.exercises_completed}
                  </div>
                </div>
              )
            })}
          </div>

          {masteryData.topic_mastery.length === 0 && (
            <div className="text-center py-12 opacity-50">
              NO MASTERY DATA YET
              <br />
              START PRACTICING TO SEE YOUR PROGRESS
            </div>
          )}
        </div>
      )}

      {/* Footer */}
      <div className="mt-8 text-center text-xs opacity-30">
        LEARNFLOW SYSTEM v1.0 | STUDENT NODE | SECURE CONNECTION
      </div>

      <style jsx>{`
        .scanlines {
          background: linear-gradient(
              rgba(18, 16, 16, 0) 50%,
              rgba(0, 0, 0, 0.1) 50%
            ),
            linear-gradient(
              90deg,
              rgba(255, 0, 0, 0.02),
              rgba(0, 255, 0, 0.01),
              rgba(0, 0, 255, 0.02)
            );
          background-size: 100% 4px, 3px 100%;
        }
      `}</style>
    </div>
  )
}
