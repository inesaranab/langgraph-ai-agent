'use client'

import React, { useState } from 'react'
import { ExternalLink, Calendar, Globe, FileText, X } from 'lucide-react'

interface Source {
  title: string
  url: string
  snippet: string
  type: 'web' | 'arxiv'
  published_date?: string
  score: number
}

interface SourceCitationProps {
  sources: Source[]
  className?: string
}

interface SourceModalProps {
  source: Source
  isOpen: boolean
  onClose: () => void
}

function SourceModal({ source, isOpen, onClose }: SourceModalProps) {
  if (!isOpen) return null

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose()
    }
  }

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      onClick={handleBackdropClick}
    >
      <div className="bg-gray-900 border border-gray-600 rounded-lg p-6 w-full max-w-2xl max-h-[80vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-2 flex-1 mr-4">
            {source.type === 'arxiv' ? (
              <FileText className="w-5 h-5 text-green-500 flex-shrink-0" />
            ) : (
              <Globe className="w-5 h-5 text-blue-500 flex-shrink-0" />
            )}
            <h3 className="text-lg font-semibold text-white line-clamp-2">{source.title}</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-md hover:bg-gray-800 text-gray-400 hover:text-gray-300"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Metadata */}
        <div className="flex items-center gap-4 mb-4 text-sm text-gray-400">
          <div className="flex items-center gap-1">
            <span className={`px-2 py-1 rounded text-xs font-medium ${
              source.type === 'arxiv' 
                ? 'bg-green-900/30 text-green-400' 
                : 'bg-blue-900/30 text-blue-400'
            }`}>
              {source.type === 'arxiv' ? 'Academic Paper' : 'Web Source'}
            </span>
          </div>
          {source.published_date && (
            <div className="flex items-center gap-1">
              <Calendar className="w-3 h-3" />
              <span>{new Date(source.published_date).toLocaleDateString()}</span>
            </div>
          )}
        </div>

        {/* Content */}
        <div className="mb-6">
          <h4 className="text-sm font-medium text-gray-300 mb-2">Preview</h4>
          <p className="text-gray-300 text-sm leading-relaxed bg-gray-800/50 p-4 rounded-lg">
            {source.snippet}
          </p>
        </div>

        {/* Actions */}
        <div className="flex gap-3">
          {source.url && (
            <a
              href={source.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              <ExternalLink className="w-4 h-4" />
              View Source
            </a>
          )}
          <button
            onClick={() => {
              navigator.clipboard.writeText(`${source.title} - ${source.url}`)
            }}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
          >
            Copy Citation
          </button>
        </div>
      </div>
    </div>
  )
}

function SourceBadge({ source, onClick }: { source: Source; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-medium transition-colors hover:scale-105 ${
        source.type === 'arxiv'
          ? 'bg-green-900/30 text-green-400 hover:bg-green-900/50'
          : 'bg-blue-900/30 text-blue-400 hover:bg-blue-900/50'
      }`}
      title={source.title}
    >
      {source.type === 'arxiv' ? (
        <FileText className="w-3 h-3" />
      ) : (
        <Globe className="w-3 h-3" />
      )}
      <span>{source.type === 'arxiv' ? 'Paper' : 'Web'}</span>
    </button>
  )
}

export default function SourceCitation({ sources, className = '' }: SourceCitationProps) {
  const [selectedSource, setSelectedSource] = useState<Source | null>(null)
  const [isExpanded, setIsExpanded] = useState(false)

  if (!sources || sources.length === 0) {
    return null
  }

  const displaySources = isExpanded ? sources : sources.slice(0, 3)
  const hasMoreSources = sources.length > 3

  return (
    <div className={`mt-4 ${className}`}>
      <div className="border-t border-gray-700 pt-3">
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-xs font-medium text-gray-400 uppercase tracking-wide">
            Sources ({sources.length})
          </h4>
          {hasMoreSources && (
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-xs text-blue-400 hover:text-blue-300 transition-colors"
            >
              {isExpanded ? 'Show Less' : `Show All ${sources.length}`}
            </button>
          )}
        </div>
        
        <div className="flex flex-wrap gap-2">
          {displaySources.map((source, index) => (
            <SourceBadge
              key={index}
              source={source}
              onClick={() => setSelectedSource(source)}
            />
          ))}
        </div>
      </div>

      <SourceModal
        source={selectedSource!}
        isOpen={selectedSource !== null}
        onClose={() => setSelectedSource(null)}
      />
    </div>
  )
}