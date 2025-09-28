'use client'

import React, { useState, useEffect } from 'react'
import { Eye, EyeOff, Key, Save, AlertCircle, ChevronDown, ChevronUp } from 'lucide-react'

interface ApiKeySettingsProps {
  onApiKeysChange: (keys: { openai: string; tavily: string }) => void
}

export default function ApiKeySettings({ onApiKeysChange }: ApiKeySettingsProps) {
  const [openaiKey, setOpenaiKey] = useState('')
  const [tavilyKey, setTavilyKey] = useState('')
  const [showOpenaiKey, setShowOpenaiKey] = useState(false)
  const [showTavilyKey, setShowTavilyKey] = useState(false)
  const [isValid, setIsValid] = useState(false)
  const [isCollapsed, setIsCollapsed] = useState(false)

  // Load from localStorage on mount
  useEffect(() => {
    const savedOpenaiKey = localStorage.getItem('openai_api_key') || ''
    const savedTavilyKey = localStorage.getItem('tavily_api_key') || ''
    
    setOpenaiKey(savedOpenaiKey)
    setTavilyKey(savedTavilyKey)
    
    // Validate keys
    const valid = savedOpenaiKey.trim() !== '' && savedTavilyKey.trim() !== ''
    setIsValid(valid)
    
    // Keep expanded if keys are not configured
    setIsCollapsed(valid)
    
    if (valid) {
      onApiKeysChange({ openai: savedOpenaiKey, tavily: savedTavilyKey })
    }
  }, [onApiKeysChange])

  const handleSave = () => {
    const trimmedOpenai = openaiKey.trim()
    const trimmedTavily = tavilyKey.trim()
    
    if (trimmedOpenai && trimmedTavily) {
      localStorage.setItem('openai_api_key', trimmedOpenai)
      localStorage.setItem('tavily_api_key', trimmedTavily)
      setIsValid(true)
      onApiKeysChange({ openai: trimmedOpenai, tavily: trimmedTavily })
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

  return (
    <div className="bg-gray-900 border border-yellow-600/30 rounded-lg p-4 scroll-mt-20">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Key className="w-4 h-4 text-yellow-500" />
          <h3 className="text-md font-semibold text-yellow-500">API Configuration</h3>
          {isValid ? (
            <span className="text-xs text-green-400">✓ Configured</span>
          ) : (
            <span className="text-xs text-red-400 bg-red-900/20 px-2 py-0.5 rounded">⚠ Required</span>
          )}
        </div>
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className={`p-2 rounded-md transition-colors ${
            !isValid && isCollapsed 
              ? 'bg-yellow-600 text-white hover:bg-yellow-700' 
              : 'hover:bg-gray-800 text-yellow-500 hover:text-yellow-400'
          }`}
          aria-label={isCollapsed ? "Expand API settings" : "Collapse API settings"}
        >
          {isCollapsed ? 
            <ChevronDown className="w-4 h-4" /> : 
            <ChevronUp className="w-4 h-4" />
          }
        </button>
      </div>
      
      {isCollapsed && !isValid && (
        <div className="p-3 bg-red-900/20 border border-red-500/30 rounded-lg">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-red-400" />
              <span className="text-sm text-red-400">API keys required to use the assistant</span>
            </div>
            <button
              onClick={() => setIsCollapsed(false)}
              className="text-xs bg-yellow-600 hover:bg-yellow-700 text-white px-3 py-1 rounded-md transition-colors"
            >
              Configure Now
            </button>
          </div>
        </div>
      )}
      
      {!isCollapsed && (
        <>
          {!isValid && (
        <div className="flex items-center gap-2 mb-3 p-2 bg-red-900/20 border border-red-500/30 rounded-lg">
          <AlertCircle className="w-4 h-4 text-red-400" />
          <span className="text-xs text-red-400">
            Please enter your API keys to start using the assistant
          </span>
        </div>
      )}

      <div className="space-y-3">
        {/* OpenAI API Key */}
        <div>
          <label className="block text-xs font-medium text-gray-300 mb-1">
            OpenAI API Key <span className="text-red-400">*</span>
          </label>
          <div className="relative">
            <input
              type={showOpenaiKey ? 'text' : 'password'}
              value={openaiKey}
              onChange={(e) => setOpenaiKey(e.target.value)}
              placeholder="sk-..."
              className="w-full bg-gray-800 border border-gray-600 rounded-md px-3 py-1.5 pr-10 text-sm text-white placeholder-gray-400 focus:border-yellow-500 focus:outline-none"
            />
            <button
              type="button"
              onClick={() => setShowOpenaiKey(!showOpenaiKey)}
              className="absolute right-2 top-2.5 text-gray-400 hover:text-gray-300"
            >
              {showOpenaiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-1">
            Get your key from <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer" className="text-yellow-500 hover:underline">OpenAI Platform</a>
          </p>
        </div>

        {/* Tavily API Key */}
        <div>
          <label className="block text-xs font-medium text-gray-300 mb-1">
            Tavily API Key <span className="text-red-400">*</span>
          </label>
          <div className="relative">
            <input
              type={showTavilyKey ? 'text' : 'password'}
              value={tavilyKey}
              onChange={(e) => setTavilyKey(e.target.value)}
              placeholder="tvly-..."
              className="w-full bg-gray-800 border border-gray-600 rounded-md px-3 py-1.5 pr-10 text-sm text-white placeholder-gray-400 focus:border-yellow-500 focus:outline-none"
            />
            <button
              type="button"
              onClick={() => setShowTavilyKey(!showTavilyKey)}
              className="absolute right-2 top-2.5 text-gray-400 hover:text-gray-300"
            >
              {showTavilyKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-1">
            Get your key from <a href="https://tavily.com/" target="_blank" rel="noopener noreferrer" className="text-yellow-500 hover:underline">Tavily</a>
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2 pt-1">
          <button
            onClick={handleSave}
            disabled={!openaiKey.trim() || !tavilyKey.trim()}
            className="flex items-center gap-1 px-3 py-1.5 text-sm bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-md transition-colors"
          >
            <Save className="w-3 h-3" />
            Save Keys
          </button>
          <button
            onClick={handleClear}
            className="px-3 py-1.5 text-sm bg-gray-700 hover:bg-gray-600 text-white rounded-md transition-colors"
          >
            Clear
          </button>
        </div>

        {isValid && (
          <div className="text-xs text-green-400 mt-1">
            ✓ API keys configured successfully
          </div>
        )}
      </div>
        </>
      )}
    </div>
  )
}