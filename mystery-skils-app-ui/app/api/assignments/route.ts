import { NextRequest, NextResponse } from 'next/server'
import { PrismaClient } from '@prisma/client'

export const dynamic = 'force-dynamic'

const prisma = new PrismaClient()

// Create assignment
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    // Support both 'level' and 'difficulty' field names for compatibility
    const { teacherId, studentId, studentName, topic, level, difficulty, type, questions } = body
    const assignmentLevel = level || difficulty || 'easy'
    const assignmentType = type || 'mcq'

    console.log('[Assignments API] Creating assignment:', { studentId, topic, type: assignmentType, level: assignmentLevel })

    const assignment = await prisma.assignment.create({
      data: {
        teacherId,
        studentId,
        studentName: studentName || 'Student',
        topic,
        level: assignmentLevel,
        type: assignmentType,
        questions: JSON.stringify(questions),
        completed: false
      }
    })

    // Create notification for student with appropriate message
    const isCoding = assignmentType === 'coding'
    const notificationTitle = isCoding ? '💻 New Coding Challenge!' : '📝 New Practice Assignment'
    const notificationMessage = isCoding
      ? `Your teacher assigned you a coding challenge: "${topic}". Go to CODE LAB to complete it!`
      : `Your teacher assigned you a practice on ${topic}`

    await prisma.notification.create({
      data: {
        userId: studentId,
        type: 'assignment',
        title: notificationTitle,
        message: notificationMessage,
        metadata: JSON.stringify({ assignmentId: assignment.id, type: assignmentType })
      }
    })

    // Create confirmation notification for teacher
    await prisma.notification.create({
      data: {
        userId: teacherId,
        type: 'confirmation',
        title: 'Assignment Sent',
        message: `${isCoding ? 'Coding challenge' : 'Practice'} on "${topic}" assigned to ${studentName || 'student'} successfully`,
        metadata: JSON.stringify({ assignmentId: assignment.id, studentId, studentName, type: assignmentType })
      }
    })

    console.log('[Assignments API] Assignment created:', assignment.id)
    return NextResponse.json({ success: true, assignment })
  } catch (error: any) {
    console.error('Create assignment error:', error)
    return NextResponse.json(
      { error: 'Failed to create assignment: ' + error.message },
      { status: 500 }
    )
  }
}
