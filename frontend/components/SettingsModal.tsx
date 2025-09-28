'use client'

import React, { useState, useEffect } from 'react'
import { X, Eye, EyeOff, Key, Save, AlertCircle, ExternalLink } from 'lucide-react'

interface SettingsModalProps {
  isOpen: boolean
  onClose: () => void
  onApiKeysChange: (keys: { openai: string; tavily: string }) => void
}

export default function SettingsModal({ isOpen, onClose, onApiKeysChange }: SettingsModalProps) {
  const [openaiKey, setOpenaiKey] = useState('')
  const [tavilyKey, setTavilyKey] = useState('')
  const [showOpenaiKey, setShowOpenaiKey] = useState(false)
  const [showTavilyKey, setShowTavilyKey] = useState(false)
  const [isValid, setIsValid] = useState(false)
  const [isSaving, setIsSaving] = useState(false)

  // Load from localStorage on mount
  useEffect(() => {
    if (isOpen) {
      const savedOpenaiKey = localStorage.getItem('openai_api_key') || ''
      const savedTavilyKey = localStorage.getItem('tavily_api_key') || ''
      
      setOpenaiKey(savedOpenaiKey)
      setTavilyKey(savedTavilyKey)
      
      // Validate keys
      const valid = savedOpenaiKey.trim() !== '' && savedTavilyKey.trim() !== ''
      setIsValid(valid)
    }
  }, [isOpen])

  const handleSave = async () => {
    const trimmedOpenai = openaiKey.trim()
    const trimmedTavily = tavilyKey.trim()
    
    if (trimmedOpenai && trimmedTavily) {
      setIsSaving(true)
      
      try {
        localStorage.setItem('openai_api_key', trimmedOpenai)
        localStorage.setItem('tavily_api_key', trimmedTavily)
        setIsValid(true)
        onApiKeysChange({ openai: trimmedOpenai, tavily: trimmedTavily })
        
        // Close modal after short delay to show success
        setTimeout(() => {
          onClose()
          setIsSaving(false)
        }, 500)
      } catch (error) {
        setIsSaving(false)
        console.error('Error saving API keys:', error)
      }
    } else {
      setIsValid(false)
    }
  }

  const handleClear = () => {
    localStorage.removeItem('openai_api_key')
    localStorage.removeItem('tavily_api_key')
    setOpenaiKey('')
    setTavilyKey('')
    setIsValid(false)
    onApiKeysChange({ openai: '', tavily: '' })
  }

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose()
    }
  }

  if (!isOpen) return null

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      onClick={handleBackdropClick}
    >
      <div className="bg-gray-900 border border-yellow-600/30 rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <Key className="w-5 h-5 text-yellow-500" />
            <h2 className="text-xl font-semibold text-yellow-500">API Settings</h2>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-md hover:bg-gray-800 text-gray-400 hover:text-gray-300"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Warning for missing keys */}
        {!isValid && (
          <div className="flex items-center gap-2 mb-6 p-4 bg-red-900/20 border border-red-500/30 rounded-lg">
            <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
            <div className="text-sm text-red-400">
              <p className="font-medium mb-1">API keys required</p>
              <p>You need both OpenAI and Tavily API keys to use the AI assistant.</p>
            </div>
          </div>
        )}

        <div className="space-y-6">
          {/* OpenAI API Key */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              OpenAI API Key <span className="text-red-400">*</span>
            </label>
            <div className="relative">
              <input
                type={showOpenaiKey ? 'text' : 'password'}
                value={openaiKey}
                onChange={(e) => setOpenaiKey(e.target.value)}
                placeholder="sk-..."
                className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-3 pr-12 text-white placeholder-gray-400 focus:border-yellow-500 focus:outline-none"
              />
              <button
                type="button"
                onClick={() => setShowOpenaiKey(!showOpenaiKey)}
                className="absolute right-3 top-3 text-gray-400 hover:text-gray-300"
              >
                {showOpenaiKey ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
            <div className="flex items-center gap-1 mt-2">
              <span className="text-xs text-gray-500">Get your key from</span>
              <a 
                href="https://platform.openai.com/api-keys" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="text-xs text-yellow-500 hover:underline flex items-center gap-1"
              >
                OpenAI Platform <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>

          {/* Tavily API Key */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Tavily API Key <span className="text-red-400">*</span>
            </label>
            <div className="relative">
              <input
                type={showTavilyKey ? 'text' : 'password'}
                value={tavilyKey}
                onChange={(e) => setTavilyKey(e.target.value)}
                placeholder="tvly-..."
                className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-3 pr-12 text-white placeholder-gray-400 focus:border-yellow-500 focus:outline-none"
              />
              <button
                type="button"
                onClick={() => setShowTavilyKey(!showTavilyKey)}
                className="absolute right-3 top-3 text-gray-400 hover:text-gray-300"
              >
                {showTavilyKey ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
            <div className="flex items-center gap-1 mt-2">
              <span className="text-xs text-gray-500">Get your key from</span>
              <a 
                href="https://tavily.com/" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="text-xs text-yellow-500 hover:underline flex items-center gap-1"
              >
                Tavily <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4">
            <button
              onClick={handleSave}
              disabled={!openaiKey.trim() || !tavilyKey.trim() || isSaving}
              className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors font-medium"
            >
              {isSaving ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <Save className="w-4 h-4" />
                  Save Keys
                </>
              )}
            </button>
            <button
              onClick={handleClear}
              disabled={isSaving}
              className="px-4 py-3 bg-gray-700 hover:bg-gray-600 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
            >
              Clear
            </button>
          </div>

          {/* Success message */}
          {isValid && !isSaving && (
            <div className="text-center text-sm text-green-400 bg-green-900/20 border border-green-500/30 rounded-lg p-3">
              ✓ API keys configured successfully
            </div>
          )}
        </div>
      </div>
    </div>
  )
}