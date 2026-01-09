import { NextRequest, NextResponse } from 'next/server'
import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

export const dynamic = 'force-dynamic'

const prisma = new PrismaClient()

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { email, password, role } = body

    if (!email || !password) {
      return NextResponse.json(
        { error: 'Email and password required' },
        { status: 400 }
      )
    }

    if (!role) {
      return NextResponse.json(
        { error: 'Role selection required' },
        { status: 400 }
      )
    }

    // Find user by email
    const user = await prisma.user.findUnique({
      where: { email }
    })

    if (!user) {
      return NextResponse.json(
        { error: 'Invalid credentials' },
        { status: 401 }
      )
    }

    // CRITICAL: Validate selected role matches registered role
    if (user.role !== role) {
      return NextResponse.json({
        success: false,
        error: `This account is registered as ${user.role.toUpperCase()}. Please select ${user.role.toUpperCase()} to login.`,
        registeredRole: user.role
      }, { status: 403 })
    }

    // Validate password - MUST match
    // Handle legacy users without password (empty string) - they need to re-register
    if (!user.password || user.password === '') {
      return NextResponse.json({
        success: false,
        error: 'Account needs password reset. Please register again with a new password.'
      }, { status: 401 })
    }

    const passwordValid = await bcrypt.compare(password, user.password)
    if (!passwordValid) {
      return NextResponse.json({
        success: false,
        error: 'Invalid password. Please check your credentials.'
      }, { status: 401 })
    }

    // Return user data only if role AND password match
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
    console.error('Login error:', error)
    return NextResponse.json(
      { error: 'Login failed: ' + error.message },
      { status: 500 }
    )
  }
}
