"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { useSession, signOut } from "@/lib/auth-client"

interface TopicMastery {
  topic_name: string
  mastery_percentage: number
  exercises_completed: number
}

interface StudentData {
  student_id: string
  overall_mastery: number
  topic_mastery: TopicMastery[]
  struggling_topics: string[]
}

export default function TeacherDashboard() {
  const router = useRouter()
  const { data: session, isPending } = useSession()
  const [students, setStudents] = useState<StudentData[]>([])
  const [backendStatus, setBackendStatus] = useState<"checking" | "online" | "offline">("checking")
  const [selectedStudent, setSelectedStudent] = useState<string | null>(null)

  useEffect(() => {
    if (!isPending && !session) {
      router.push("/auth")
    } else if ((session?.user as any)?.role !== "teacher") {
      router.push("/student") // Redirect non-teachers
    }
  }, [session, isPending, router])

  useEffect(() => {
    if ((session?.user as any)?.role === "teacher") {
      checkBackendStatus()
      fetchAllStudents()
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

  const fetchAllStudents = async () => {
    try {
      // For demo, fetch known students
      // In production, you'd have an endpoint that lists all students
      const studentIds = ["demo-student-001", "demo-student-002", "demo-student-003"]

      const studentDataPromises = studentIds.map(async (id) => {
        try {
          const response = await fetch(`http://localhost:8006/api/v1/mastery/${id}`)
          return await response.json()
        } catch (error) {
          return null
        }
      })

      const results = await Promise.all(studentDataPromises)
      setStudents(results.filter((s) => s !== null && s.topic_mastery?.length > 0))
    } catch (error) {
      console.error("Failed to fetch students:", error)
    }
  }

  const handleSignOut = async () => {
    await signOut()
    router.push("/auth")
  }

  const getColorForPercentage = (percent: number) => {
    if (percent >= 70) return "#39ff14"
    if (percent >= 40) return "#ffaa00"
    return "#ff3131"
  }

  const getStatusLabel = (percent: number) => {
    if (percent >= 70) return "EXCELLENT"
    if (percent >= 40) return "PROGRESSING"
    return "NEEDS ATTENTION"
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

  const selectedStudentData = students.find((s) => s.student_id === selectedStudent)

  return (
    <div className="min-h-screen bg-black text-[#00ffcc] font-mono p-8">
      {/* Scanlines Overlay */}
      <div className="scanlines fixed inset-0 pointer-events-none opacity-30 z-50" />

      {/* Header */}
      <div className="mb-8 border border-[#00ffcc] p-6 bg-black/75 backdrop-blur-sm">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h1 className="text-3xl font-bold mb-2">TEACHER CONTROL PANEL</h1>
            <div className="text-sm opacity-70">
              INSTRUCTOR: {session.user?.email?.toUpperCase()}
            </div>
            {(session.user as any)?.teacherId && (
              <div className="text-xs opacity-50">
                ID: {(session.user as any).teacherId}
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

        <div className="flex items-center gap-4">
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
          <div className="border-l border-[#00ffcc] pl-4">
            <span>TOTAL STUDENTS: {students.length}</span>
          </div>
        </div>
      </div>

      {/* Class Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {students.map((student) => {
          const overallPercent = Math.round(student.overall_mastery * 100)
          const color = getColorForPercentage(overallPercent)
          const status = getStatusLabel(overallPercent)

          return (
            <div
              key={student.student_id}
              onClick={() => setSelectedStudent(student.student_id)}
              className="border border-[#00ffcc] p-6 bg-black/75 backdrop-blur-sm cursor-pointer hover:border-[#39ff14] transition-colors"
            >
              <div className="text-sm opacity-50 mb-2">STUDENT ID:</div>
              <div className="text-lg font-bold mb-4">
                {student.student_id.toUpperCase()}
              </div>

              <div className="text-4xl font-bold mb-2" style={{ color }}>
                {overallPercent}%
              </div>

              <div className="w-full bg-gray-800 h-3 mb-4">
                <div
                  style={{ width: `${overallPercent}%`, backgroundColor: color }}
                  className="h-3"
                />
              </div>

              <div style={{ color }} className="font-bold mb-3">
                {status}
              </div>

              {student.struggling_topics.length > 0 && (
                <div className="text-[#ff3131] text-sm">
                  ⚠ {student.struggling_topics.length} struggling topic(s)
                </div>
              )}

              <div className="text-xs opacity-50 mt-3">
                CLICK FOR DETAILS
              </div>
            </div>
          )
        })}

        {students.length === 0 && (
          <div className="col-span-3 border border-[#00ffcc] p-12 bg-black/75 backdrop-blur-sm text-center opacity-50">
            NO STUDENT DATA AVAILABLE
            <br />
            WAITING FOR STUDENTS TO START PRACTICING
          </div>
        )}
      </div>

      {/* Selected Student Details */}
      {selectedStudentData && (
        <div className="border border-[#39ff14] p-6 bg-black/75 backdrop-blur-sm">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl text-[#39ff14]">
              STUDENT DETAILS: {selectedStudentData.student_id.toUpperCase()}
            </h2>
            <button
              onClick={() => setSelectedStudent(null)}
              className="border border-[#00ffcc] px-4 py-2 hover:bg-[#00ffcc] hover:text-black transition-colors text-sm"
            >
              CLOSE
            </button>
          </div>

          <div className="space-y-6">
            {selectedStudentData.topic_mastery.map((topic) => {
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
                      className="h-3"
                    />
                  </div>
                  <div className="text-xs opacity-50">
                    EXERCISES: {topic.exercises_completed}
                  </div>
                </div>
              )
            })}
          </div>

          {selectedStudentData.struggling_topics.length > 0 && (
            <div className="mt-6 p-4 border border-[#ff3131]">
              <div className="text-[#ff3131] font-bold mb-3">
                ⚠ INTERVENTION REQUIRED - STRUGGLING TOPICS:
              </div>
              {selectedStudentData.struggling_topics.map((topic) => (
                <div key={topic} className="text-[#ff3131] ml-4">
                  • {topic.toUpperCase().replace(/-/g, " ")}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Footer */}
      <div className="mt-8 text-center text-xs opacity-30">
        LEARNFLOW SYSTEM v1.0 | TEACHER NODE | ADMINISTRATOR ACCESS
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
