import { NextRequest, NextResponse } from 'next/server'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ userId: string }> }
) {
  try {
    const { userId } = await params
    const body = await request.json()
    const { notificationId } = body

    await prisma.notification.update({
      where: { id: notificationId },
      data: { read: true }
    })

    return NextResponse.json({ success: true })
  } catch (error: any) {
    console.error('Mark notification read error:', error)
    return NextResponse.json(
      { error: 'Failed to mark notification read: ' + error.message },
      { status: 500 }
    )
  }
}
