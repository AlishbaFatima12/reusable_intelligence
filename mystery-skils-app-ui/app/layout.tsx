import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Mystery Skills - 3D Learning Mastery Platform',
  description: 'Real-time visualization of student learning progress with AI agent monitoring',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}
