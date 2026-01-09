"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { signIn, signUp } from "@/lib/auth-client"

export default function AuthPage() {
  const router = useRouter()
  const [isLogin, setIsLogin] = useState(true)
  const [role, setRole] = useState<"student" | "teacher">("student")
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  })
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setLoading(true)

    try {
      if (isLogin) {
        // Login
        const result = await signIn.email({
          email: formData.email,
          password: formData.password,
        })

        if (result.error) {
          setError(result.error.message || "Login failed")
          setLoading(false)
          return
        }

        // Redirect based on role
        const user = result.data?.user as any
        if (user?.role === "teacher") {
          router.push("/teacher")
        } else {
          router.push("/student")
        }
      } else {
        // Sign up
        const studentId = role === "student" ? `student-${Date.now()}` : undefined
        const teacherId = role === "teacher" ? `teacher-${Date.now()}` : undefined

        const result = await signUp.email({
          email: formData.email,
          password: formData.password,
          name: formData.name,
          role,
          studentId,
          teacherId,
        })

        if (result.error) {
          setError(result.error.message || "Signup failed")
          setLoading(false)
          return
        }

        // Redirect based on role
        if (role === "teacher") {
          router.push("/teacher")
        } else {
          router.push("/student")
        }
      }
    } catch (err: any) {
      setError(err.message || "An error occurred")
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-black text-green-400 flex items-center justify-center font-mono p-4">
      <div className="w-full max-w-md">
        <div className="border border-green-400 p-8 space-y-6">
          <div className="text-center">
            <h1 className="text-2xl mb-2">LEARNFLOW SYSTEM</h1>
            <div className="text-sm opacity-70">
              {isLogin ? "AUTHENTICATION" : "REGISTRATION"}
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <div>
                <label className="block text-sm mb-2">NAME:</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) =>
                    setFormData({ ...formData, name: e.target.value })
                  }
                  className="w-full bg-black border border-green-400 p-2 text-green-400 focus:outline-none focus:border-green-300"
                  required={!isLogin}
                  disabled={loading}
                />
              </div>
            )}

            <div>
              <label className="block text-sm mb-2">EMAIL:</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) =>
                  setFormData({ ...formData, email: e.target.value })
                }
                className="w-full bg-black border border-green-400 p-2 text-green-400 focus:outline-none focus:border-green-300"
                required
                disabled={loading}
              />
            </div>

            <div>
              <label className="block text-sm mb-2">PASSWORD:</label>
              <input
                type="password"
                value={formData.password}
                onChange={(e) =>
                  setFormData({ ...formData, password: e.target.value })
                }
                className="w-full bg-black border border-green-400 p-2 text-green-400 focus:outline-none focus:border-green-300"
                required
                disabled={loading}
                minLength={8}
              />
            </div>

            {!isLogin && (
              <div>
                <label className="block text-sm mb-2">ROLE:</label>
                <div className="flex gap-4">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      name="role"
                      value="student"
                      checked={role === "student"}
                      onChange={(e) => setRole("student")}
                      className="form-radio text-green-400"
                      disabled={loading}
                    />
                    <span>STUDENT</span>
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      name="role"
                      value="teacher"
                      checked={role === "teacher"}
                      onChange={(e) => setRole("teacher")}
                      className="form-radio text-green-400"
                      disabled={loading}
                    />
                    <span>TEACHER</span>
                  </label>
                </div>
              </div>
            )}

            {error && (
              <div className="text-red-400 text-sm border border-red-400 p-2">
                ERROR: {error}
              </div>
            )}

            <button
              type="submit"
              className="w-full border border-green-400 p-3 hover:bg-green-400 hover:text-black transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={loading}
            >
              {loading ? "PROCESSING..." : isLogin ? "LOGIN" : "REGISTER"}
            </button>
          </form>

          <div className="text-center">
            <button
              onClick={() => {
                setIsLogin(!isLogin)
                setError("")
              }}
              className="text-sm hover:text-green-300 transition-colors"
              disabled={loading}
            >
              {isLogin
                ? "NEED AN ACCOUNT? REGISTER"
                : "HAVE AN ACCOUNT? LOGIN"}
            </button>
          </div>

          <div className="text-xs opacity-50 text-center pt-4 border-t border-green-400">
            SYSTEM VERSION 1.0 | SECURE CONNECTION ESTABLISHED
          </div>
        </div>
      </div>
    </div>
  )
}
