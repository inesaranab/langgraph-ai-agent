import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'LangGraph AI Agent',
  description: 'Intelligent AI agent powered by LangGraph',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-dark-50">
          {children}
        </div>
      </body>
    </html>
  )
}