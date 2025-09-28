'use client'

import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'

interface MarkdownRendererProps {
  content: string
  className?: string
}

export default function MarkdownRenderer({ content, className = "" }: MarkdownRendererProps) {
  return (
    <div className={`markdown-content ${className}`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          // Code blocks
          code({ node, className, children, ...props }: any) {
            const match = /language-(\w+)/.exec(className || '')
            const inline = !match
            return !inline && match ? (
              <SyntaxHighlighter
                style={oneDark}
                language={match[1]}
                PreTag="div"
                customStyle={{
                  margin: '1rem 0',
                  borderRadius: '0.5rem',
                  fontSize: '0.875rem'
                }}
                {...props}
              >
                {String(children).replace(/\n$/, '')}
              </SyntaxHighlighter>
            ) : (
              <code 
                className="bg-dark-200 text-primary-600 px-1.5 py-0.5 rounded text-sm font-mono" 
                {...props}
              >
                {children}
              </code>
            )
          },
          
          // Headings
          h1: ({ children }) => (
            <h1 className="text-xl font-bold text-dark-800 mb-3 mt-4 first:mt-0">
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-lg font-semibold text-dark-800 mb-2 mt-3 first:mt-0">
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-base font-medium text-dark-700 mb-2 mt-3 first:mt-0">
              {children}
            </h3>
          ),
          
          // Paragraphs
          p: ({ children }) => (
            <p className="mb-3 leading-relaxed text-dark-700">
              {children}
            </p>
          ),
          
          // Lists
          ul: ({ children }) => (
            <ul className="list-none mb-3 space-y-1">
              {children}
            </ul>
          ),
          li: ({ children }) => (
            <li className="flex items-start space-x-2">
              <span className="w-1.5 h-1.5 bg-primary-500 rounded-full mt-2 flex-shrink-0"></span>
              <span className="text-dark-700">{children}</span>
            </li>
          ),
          
          // Ordered lists
          ol: ({ children }) => (
            <ol className="list-decimal list-inside mb-3 space-y-1 text-dark-700">
              {children}
            </ol>
          ),
          
          // Links
          a: ({ children, href }) => (
            <a 
              href={href}
              className="text-primary-600 hover:text-primary-700 underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              {children}
            </a>
          ),
          
          // Blockquotes
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-primary-500 pl-4 my-3 italic text-dark-600">
              {children}
            </blockquote>
          ),
          
          // Horizontal rule
          hr: () => (
            <hr className="border-dark-300 my-4" />
          ),
          
          // Tables
          table: ({ children }) => (
            <div className="overflow-x-auto my-3">
              <table className="min-w-full border border-dark-300 rounded-lg">
                {children}
              </table>
            </div>
          ),
          th: ({ children }) => (
            <th className="bg-dark-200 border border-dark-300 px-3 py-2 text-left font-medium text-dark-800">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="border border-dark-300 px-3 py-2 text-dark-700">
              {children}
            </td>
          ),
          
          // Strong and emphasis
          strong: ({ children }) => (
            <strong className="font-semibold text-dark-800">{children}</strong>
          ),
          em: ({ children }) => (
            <em className="italic text-dark-700">{children}</em>
          )
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}