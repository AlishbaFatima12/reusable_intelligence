import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Mystery Skills - LearnFlow Platform',
  description: '3D Learning Mastery Visualization with AI Agent Monitoring',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-matrix-bg text-white antialiased">{children}</body>
    </html>
  );
}
