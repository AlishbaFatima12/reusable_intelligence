import { NextRequest, NextResponse } from 'next/server'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// Create assignment
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { teacherId, studentId, studentName, topic, level, questions } = body

    const assignment = await prisma.assignment.create({
      data: {
        teacherId,
        studentId,
        studentName,
        topic,
        level,
        questions: JSON.stringify(questions),
        completed: false
      }
    })

    // Create notification for student
    await prisma.notification.create({
      data: {
        userId: studentId,
        type: 'assignment',
        title: 'New Practice Assignment',
        message: `Your teacher assigned you a practice on ${topic}`,
        metadata: JSON.stringify({ assignmentId: assignment.id })
      }
    })

    // Create confirmation notification for teacher
    await prisma.notification.create({
      data: {
        userId: teacherId,
        type: 'confirmation',
        title: 'Assignment Sent',
        message: `Practice on "${topic}" assigned to ${studentName} successfully`,
        metadata: JSON.stringify({ assignmentId: assignment.id, studentId, studentName })
      }
    })

    return NextResponse.json({ success: true, assignment })
  } catch (error: any) {
    console.error('Create assignment error:', error)
    return NextResponse.json(
      { error: 'Failed to create assignment: ' + error.message },
      { status: 500 }
    )
  }
}
