import { NextRequest, NextResponse } from 'next/server'
import prisma from '@/lib/prisma'

export const dynamic = 'force-dynamic'
export const runtime = 'nodejs'

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ userId: string }> }
) {
  try {
    const { userId } = await params

    // Detect role from userId pattern
    const isTeacher = userId.startsWith('teacher-')
    const isStudent = userId.startsWith('student-')

    console.log(`[Notifications API] ====== REQUEST ======`)
    console.log(`[Notifications API] userId=${userId}`)
    console.log(`[Notifications API] isTeacher=${isTeacher}, isStudent=${isStudent}`)
    console.log(`[Notifications API] Filtering by types:`, isTeacher ? ['completion', 'confirmation', 'registration'] : isStudent ? ['assignment', 'reminder', 'appreciation', 'encouragement', 'achievement'] : 'UNKNOWN ROLE')

    let notifications: any[] = []

    if (isTeacher) {
      // TEACHER: Only show notifications specifically for teachers
      // Types: completion (student finished), confirmation (assignment sent), registration (new student)
      notifications = await prisma.notification.findMany({
        where: {
          AND: [
            { userId: userId },
            {
              type: {
                in: ['completion', 'confirmation', 'registration']
              }
            }
          ]
        },
        orderBy: {
          createdAt: 'desc'
        }
      })
      console.log(`[Notifications API] Teacher ${userId} has ${notifications.length} notifications`)
      if (notifications.length > 0) {
        console.log(`[Notifications API] First notification:`, { id: notifications[0].id, type: notifications[0].type, title: notifications[0].title })
      }
    } else if (isStudent) {
      // STUDENT: Only show notifications specifically for this student
      // Types: assignment, reminder, appreciation, encouragement, achievement
      notifications = await prisma.notification.findMany({
        where: {
          AND: [
            { userId: userId },
            {
              type: {
                in: ['assignment', 'reminder', 'appreciation', 'encouragement', 'achievement']
              }
            }
          ]
        },
        orderBy: {
          createdAt: 'desc'
        }
      })
      console.log(`[Notifications API] Student ${userId} has ${notifications.length} notifications`)
      if (notifications.length > 0) {
        console.log(`[Notifications API] First notification:`, { id: notifications[0].id, type: notifications[0].type, title: notifications[0].title })
      }
    } else {
      // Unknown role - return empty
      console.log(`[Notifications API] Unknown role for userId=${userId}`)
      notifications = []
    }

    const unreadCount = notifications.filter(n => !n.read).length

    return NextResponse.json({
      success: true,
      notifications,
      unreadCount,
      debug: { userId, isTeacher, isStudent, count: notifications.length }
    })
  } catch (error: any) {
    console.error('Get notifications error:', error)
    return NextResponse.json(
      { error: 'Failed to get notifications: ' + error.message },
      { status: 500 }
    )
  }
}
