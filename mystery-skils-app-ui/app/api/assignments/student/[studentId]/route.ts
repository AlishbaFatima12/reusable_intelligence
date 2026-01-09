import { NextRequest, NextResponse } from 'next/server'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ studentId: string }> }
) {
  try {
    const { studentId } = await params
    const assignments = await prisma.assignment.findMany({
      where: {
        studentId: studentId
      },
      orderBy: {
        createdAt: 'desc'
      }
    })

    // Parse questions JSON
    const assignmentsWithQuestions = assignments.map(a => ({
      ...a,
      questions: JSON.parse(a.questions)
    }))

    return NextResponse.json({ success: true, assignments: assignmentsWithQuestions })
  } catch (error: any) {
    console.error('Get assignments error:', error)
    return NextResponse.json(
      { error: 'Failed to get assignments: ' + error.message },
      { status: 500 }
    )
  }
}
