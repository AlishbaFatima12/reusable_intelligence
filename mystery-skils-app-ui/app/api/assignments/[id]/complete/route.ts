import { NextRequest, NextResponse } from 'next/server'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params
    const body = await request.json()
    const { score, studentName } = body

    const assignment = await prisma.assignment.update({
      where: { id: id },
      data: {
        completed: true,
        score,
        completedAt: new Date()
      }
    })

    // Get topic and teacher
    const { teacherId, topic } = assignment

    // Create notification for teacher
    await prisma.notification.create({
      data: {
        userId: teacherId,
        type: 'completion',
        title: score === 100 ? '🏆 Perfect Score!' : 'Student Completed Practice',
        message: score === 100
          ? `Congratulations! ${studentName} achieved 100% on ${topic}! Outstanding performance!`
          : `${studentName} completed ${topic} with score ${score}%`,
        metadata: JSON.stringify({ assignmentId: assignment.id, score, isPerfect: score === 100 })
      }
    })

    // If student got 100%, also create an appreciation notification for the student
    if (score === 100) {
      await prisma.notification.create({
        data: {
          userId: assignment.studentId,
          type: 'achievement',
          title: '🏆 Perfect Score Achievement!',
          message: `Amazing! You scored 100% on ${topic}! Your teacher is proud of you!`,
          metadata: JSON.stringify({ assignmentId: assignment.id, topic })
        }
      })
    }

    return NextResponse.json({ success: true, assignment })
  } catch (error: any) {
    console.error('Complete assignment error:', error)
    return NextResponse.json(
      { error: 'Failed to complete assignment: ' + error.message },
      { status: 500 }
    )
  }
}
