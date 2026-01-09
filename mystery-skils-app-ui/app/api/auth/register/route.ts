import { NextRequest, NextResponse } from 'next/server'
import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { name, email, password, role } = body

    if (!name || !email || !password) {
      return NextResponse.json(
        { error: 'Name, email and password required' },
        { status: 400 }
      )
    }

    // Check if user already exists
    const existing = await prisma.user.findUnique({
      where: { email }
    })

    if (existing) {
      return NextResponse.json(
        { error: 'Email already registered' },
        { status: 400 }
      )
    }

    // Create user
    const userRole = role || 'student'
    const studentId = userRole === 'student' ? `student-${Date.now()}` : null
    const teacherId = userRole === 'teacher' ? `teacher-${Date.now()}` : null

    // Hash password before storing
    const hashedPassword = await bcrypt.hash(password, 10)

    const user = await prisma.user.create({
      data: {
        id: `user-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        email,
        name,
        password: hashedPassword,
        emailVerified: true, // Skip email verification for demo
        role: userRole,
        studentId,
        teacherId,
        createdAt: new Date(),
        updatedAt: new Date()
      }
    })

    // If a new student registered, create notification for all teachers
    if (userRole === 'student' && studentId) {
      // Get all teachers
      const teachers = await prisma.user.findMany({
        where: { role: 'teacher' },
        select: { teacherId: true }
      })

      // Create notification for each teacher about new student
      const notificationPromises = teachers.map(teacher => {
        if (teacher.teacherId) {
          return prisma.notification.create({
            data: {
              id: `notif-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
              userId: teacher.teacherId,
              type: 'registration',
              title: 'New Student Registered',
              message: `${name} just joined the platform`,
              read: false,
              createdAt: new Date(),
              metadata: JSON.stringify({ studentId, studentName: name, email })
            }
          })
        }
        return null
      })

      // Also create a generic registration notification (for teachers with any ID)
      notificationPromises.push(
        prisma.notification.create({
          data: {
            id: `notif-${Date.now()}-${Math.random().toString(36).substr(2, 9)}-broadcast`,
            userId: 'all-teachers',  // Special marker for broadcast notifications
            type: 'registration',
            title: 'New Student Registered',
            message: `${name} just joined the platform`,
            read: false,
            createdAt: new Date(),
            metadata: JSON.stringify({ studentId, studentName: name, email })
          }
        })
      )

      await Promise.all(notificationPromises.filter(Boolean))
    }

    return NextResponse.json({
      success: true,
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role,
        studentId: user.studentId,
        teacherId: user.teacherId
      }
    })

  } catch (error: any) {
    console.error('Registration error:', error)
    return NextResponse.json(
      { error: 'Registration failed: ' + error.message },
      { status: 500 }
    )
  }
}
