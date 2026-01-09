import { NextRequest, NextResponse } from 'next/server'
import prisma from '@/lib/prisma'

export const dynamic = 'force-dynamic'
export const runtime = 'nodejs'

// POST - Create a new notification
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { userId, type, title, message, metadata } = body

    console.log(`[Notifications API] ====== CREATE ======`)
    console.log(`[Notifications API] Creating notification for userId=${userId}, type=${type}`)
    console.log(`[Notifications API] Title: ${title}`)

    if (!userId || !type || !title || !message) {
      return NextResponse.json(
        { error: 'userId, type, title, and message are required' },
        { status: 400 }
      )
    }

    const notification = await prisma.notification.create({
      data: {
        id: `notif-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        userId,
        type,
        title,
        message,
        read: false,
        createdAt: new Date(),
        metadata: metadata || null
      }
    })

    console.log(`[Notifications API] Created notification ID=${notification.id} for userId=${notification.userId}`)

    return NextResponse.json({
      success: true,
      notification
    })

  } catch (error: any) {
    console.error('Create notification error:', error)
    return NextResponse.json(
      { error: 'Failed to create notification: ' + error.message },
      { status: 500 }
    )
  }
}
