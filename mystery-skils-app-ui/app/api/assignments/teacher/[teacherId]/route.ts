import { NextRequest, NextResponse } from 'next/server'
import { PrismaClient } from '@prisma/client'

export const dynamic = 'force-dynamic'

const prisma = new PrismaClient()

// Get all assignments (for demo - shows all regardless of teacher ID)
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ teacherId: string }> }
) {
  try {
    const { teacherId } = await params

    // For demo: get ALL assignments to show across all teachers
    const assignments = await prisma.assignment.findMany({
      orderBy: { createdAt: 'desc' }
    })

    // Parse questions JSON for each assignment
    const parsed = assignments.map(a => ({
      ...a,
      questions: JSON.parse(a.questions)
    }))

    // Calculate stats
    const totalAssigned = assignments.length
    const totalCompleted = assignments.filter(a => a.completed).length
    const totalPending = totalAssigned - totalCompleted
    const completedWithScores = assignments.filter(a => a.completed && a.score !== null)
    const avgScore = completedWithScores.length > 0
      ? Math.round(completedWithScores.reduce((sum, a) => sum + (a.score || 0), 0) / completedWithScores.length)
      : 0

    // Recent submissions (completed assignments)
    const recentSubmissions = assignments
      .filter(a => a.completed)
      .slice(0, 10)
      .map(a => ({
        id: a.id,
        studentName: a.studentName,
        topic: a.topic,
        score: a.score,
        completedAt: a.completedAt
      }))

    return NextResponse.json({
      success: true,
      stats: {
        totalAssigned,
        totalCompleted,
        totalPending,
        avgScore
      },
      recentSubmissions,
      assignments: parsed
    })
  } catch (error: any) {
    console.error('Get teacher assignments error:', error)
    return NextResponse.json(
      { error: 'Failed to get assignments: ' + error.message },
      { status: 500 }
    )
  }
}
