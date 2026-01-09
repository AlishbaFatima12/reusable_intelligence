import { NextRequest, NextResponse } from 'next/server'
import prisma from '@/lib/prisma'

export const dynamic = 'force-dynamic'
export const runtime = 'nodejs'

export async function GET(request: NextRequest) {
  try {
    // Fetch all students from the database
    const students = await prisma.user.findMany({
      where: {
        role: 'student'
      },
      select: {
        id: true,
        name: true,
        email: true,
        studentId: true,
        role: true,
        createdAt: true
      },
      orderBy: {
        createdAt: 'desc'
      }
    })

    return NextResponse.json({
      success: true,
      students
    })

  } catch (error: any) {
    console.error('Failed to fetch students:', error)
    return NextResponse.json(
      { error: 'Failed to fetch students: ' + error.message },
      { status: 500 }
    )
  }
}
