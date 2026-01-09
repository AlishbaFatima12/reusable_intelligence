import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Mystery Skills - The Learning Revolution by Syeda Alishba Fatima',
  description: 'Real-time visualization of student learning progress with AI agent monitoring',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="antialiased" suppressHydrationWarning>
        {children}
      </body>
    </html>
  )
}
