'use client'

import React, { useState, useEffect } from 'react'
import { X, ExternalLink, Calendar, Globe, FileText, Search, Filter, Clock, Star } from 'lucide-react'
import { Source } from '../lib/chatService'

interface SourcesPanelProps {
  isOpen: boolean
  onClose: () => void
  allSources: Source[]
  className?: string
}

interface SourceWithMetadata extends Source {
  messageIndex: number
  query: string
  timestamp: Date
}

export default function SourcesPanel({ isOpen, onClose, allSources, className = '' }: SourcesPanelProps) {
  const [filteredSources, setFilteredSources] = useState<SourceWithMetadata[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [typeFilter, setTypeFilter] = useState<'all' | 'web' | 'arxiv'>('all')
  const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'relevance'>('newest')

  // Process and filter sources
  useEffect(() => {
    let processed = allSources.map((source, index) => ({
      ...source,
      messageIndex: Math.floor(index / 3), // Rough approximation
      query: 'Research Query',
      timestamp: new Date(Date.now() - (allSources.length - index) * 60000) // Mock timestamps
    }))

    // Apply search filter
    if (searchTerm) {
      processed = processed.filter(source =>
        source.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        source.snippet.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Apply type filter
    if (typeFilter !== 'all') {
      processed = processed.filter(source => source.type === typeFilter)
    }

    // Apply sorting
    processed.sort((a, b) => {
      switch (sortBy) {
        case 'newest':
          return b.timestamp.getTime() - a.timestamp.getTime()
        case 'oldest':
          return a.timestamp.getTime() - b.timestamp.getTime()
        case 'relevance':
          return b.score - a.score
        default:
          return 0
      }
    })

    setFilteredSources(processed)
  }, [allSources, searchTerm, typeFilter, sortBy])

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose()
    }
  }

  const getTypeColor = (type: string) => {
    return type === 'arxiv' ? 'text-green-400' : 'text-blue-400'
  }

  const getTypeBg = (type: string) => {
    return type === 'arxiv' ? 'bg-green-900/30' : 'bg-blue-900/30'
  }

  if (!isOpen) return null

  const webCount = allSources.filter(s => s.type === 'web').length
  const arxivCount = allSources.filter(s => s.type === 'arxiv').length

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      onClick={handleBackdropClick}
    >
      <div className="bg-gray-900 border border-gray-600 rounded-lg w-full max-w-4xl h-[85vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-700">
          <div className="flex items-center gap-3">
            <Search className="w-6 h-6 text-yellow-500" />
            <div>
              <h2 className="text-xl font-semibold text-white">Research Sources</h2>
              <p className="text-sm text-gray-400">
                {allSources.length} sources • {webCount} web • {arxivCount} academic
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-md hover:bg-gray-800 text-gray-400 hover:text-gray-300"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Controls */}
        <div className="p-4 border-b border-gray-700 bg-gray-800/50">
          <div className="flex flex-wrap gap-4 items-center">
            {/* Search */}
            <div className="flex-1 min-w-64">
              <div className="relative">
                <Search className="w-4 h-4 absolute left-3 top-3 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search sources..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg pl-10 pr-4 py-2 text-white placeholder-gray-400 focus:border-yellow-500 focus:outline-none"
                />
              </div>
            </div>

            {/* Type Filter */}
            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-gray-400" />
              <select
                value={typeFilter}
                onChange={(e) => setTypeFilter(e.target.value as any)}
                className="bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:border-yellow-500 focus:outline-none"
              >
                <option value="all">All Sources</option>
                <option value="web">Web Sources</option>
                <option value="arxiv">Academic Papers</option>
              </select>
            </div>

            {/* Sort */}
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-gray-400" />
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:border-yellow-500 focus:outline-none"
              >
                <option value="newest">Newest First</option>
                <option value="oldest">Oldest First</option>
                <option value="relevance">Most Relevant</option>
              </select>
            </div>
          </div>
        </div>

        {/* Sources List */}
        <div className="flex-1 overflow-y-auto p-4">
          {filteredSources.length === 0 ? (
            <div className="text-center py-12">
              <Search className="w-12 h-12 text-gray-600 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-400 mb-2">No sources found</h3>
              <p className="text-gray-500">
                {allSources.length === 0 
                  ? 'Start a conversation to see research sources appear here.'
                  : 'Try adjusting your search or filter criteria.'
                }
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredSources.map((source, index) => (
                <div 
                  key={index}
                  className="bg-gray-800/50 border border-gray-700 rounded-lg p-4 hover:bg-gray-800/70 transition-colors"
                >
                  {/* Source Header */}
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-start gap-3 flex-1">
                      <div className={`p-2 rounded-lg ${getTypeBg(source.type)}`}>
                        {source.type === 'arxiv' ? (
                          <FileText className={`w-4 h-4 ${getTypeColor(source.type)}`} />
                        ) : (
                          <Globe className={`w-4 h-4 ${getTypeColor(source.type)}`} />
                        )}
                      </div>
                      
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-white mb-1 line-clamp-2">
                          {source.title}
                        </h3>
                        <div className="flex items-center gap-4 text-xs text-gray-400 mb-2">
                          <span className={`px-2 py-1 rounded ${getTypeBg(source.type)} ${getTypeColor(source.type)}`}>
                            {source.type === 'arxiv' ? 'Academic Paper' : 'Web Source'}
                          </span>
                          {source.published_date && (
                            <div className="flex items-center gap-1">
                              <Calendar className="w-3 h-3" />
                              <span>{new Date(source.published_date).toLocaleDateString()}</span>
                            </div>
                          )}
                          <div className="flex items-center gap-1">
                            <Star className="w-3 h-3" />
                            <span>{Math.round(source.score * 100)}% relevance</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="flex gap-2 ml-4">
                      {source.url && (
                        <a
                          href={source.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="p-2 rounded-md hover:bg-gray-700 text-gray-400 hover:text-white transition-colors"
                          title="Open source"
                        >
                          <ExternalLink className="w-4 h-4" />
                        </a>
                      )}
                    </div>
                  </div>

                  {/* Source Snippet */}
                  <p className="text-gray-300 text-sm leading-relaxed line-clamp-3">
                    {source.snippet}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-700 bg-gray-800/50">
          <div className="flex items-center justify-between text-sm text-gray-400">
            <span>Showing {filteredSources.length} of {allSources.length} sources</span>
            <button
              onClick={() => {
                setSearchTerm('')
                setTypeFilter('all')
                setSortBy('newest')
              }}
              className="text-yellow-500 hover:text-yellow-400 transition-colors"
            >
              Clear Filters
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}