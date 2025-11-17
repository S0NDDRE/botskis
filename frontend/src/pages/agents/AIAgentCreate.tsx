import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { agentsAPI } from '../../lib/api'
import { useNavigate } from 'react-router-dom'
import { Bot, Sparkles, CheckCircle, XCircle } from 'lucide-react'
import toast from 'react-hot-toast'

export default function AIAgentCreate() {
  const navigate = useNavigate()
  const [description, setDescription] = useState('')
  const [generatedAgent, setGeneratedAgent] = useState<any>(null)
  const [testInput, setTestInput] = useState('')
  const [testResult, setTestResult] = useState<any>(null)

  const generateMutation = useMutation({
    mutationFn: (desc: string) => agentsAPI.generateAgent(desc),
    onSuccess: (response) => {
      setGeneratedAgent(response.data)
      toast.success('Agent generated successfully!')
    },
    onError: () => {
      toast.error('Failed to generate agent')
    },
  })

  const testMutation = useMutation({
    mutationFn: (input: string) => agentsAPI.testAgent(generatedAgent.id, { input }),
    onSuccess: (response) => {
      setTestResult(response.data)
    },
  })

  const deployMutation = useMutation({
    mutationFn: () => agentsAPI.deployAgent(generatedAgent.id),
    onSuccess: () => {
      toast.success('Agent deployed successfully!')
      navigate('/agents')
    },
  })

  const handleGenerate = () => {
    if (!description.trim()) return
    generateMutation.mutate(description)
  }

  const handleTest = () => {
    if (!testInput.trim()) return
    testMutation.mutate(testInput)
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Create AI Agent
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Describe what you want your AI agent to do in plain language
        </p>
      </div>

      {/* Step 1: Describe */}
      <div className="card p-6">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 font-bold flex items-center justify-center">
            1
          </div>
          <h2 className="text-xl font-semibold">Describe Your Agent</h2>
        </div>

        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Example: Create an agent that automatically responds to customer emails with helpful information..."
          rows={6}
          className="w-full input mb-4"
          disabled={!!generatedAgent}
        />

        {!generatedAgent && (
          <button
            onClick={handleGenerate}
            disabled={generateMutation.isPending || !description.trim()}
            className="btn-primary flex items-center gap-2"
          >
            <Sparkles className="w-4 h-4" />
            {generateMutation.isPending ? 'Generating...' : 'Generate Agent'}
          </button>
        )}
      </div>

      {/* Step 2: Review */}
      {generatedAgent && (
        <div className="card p-6">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 font-bold flex items-center justify-center">
              2
            </div>
            <h2 className="text-xl font-semibold">Review Generated Agent</h2>
          </div>

          <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-6 mb-4">
            <h3 className="font-semibold text-lg mb-2">{generatedAgent.name}</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              {generatedAgent.description}
            </p>

            <div className="space-y-2">
              <h4 className="font-medium text-sm text-gray-700 dark:text-gray-300">
                Capabilities:
              </h4>
              <ul className="list-disc list-inside space-y-1 text-sm text-gray-600 dark:text-gray-400">
                {generatedAgent.capabilities?.map((cap: string, i: number) => (
                  <li key={i}>{cap}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* Test Agent */}
          <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
            <h4 className="font-medium mb-3">Test Your Agent</h4>
            <div className="flex gap-2 mb-4">
              <input
                type="text"
                value={testInput}
                onChange={(e) => setTestInput(e.target.value)}
                placeholder="Enter test input..."
                className="flex-1 input"
              />
              <button
                onClick={handleTest}
                disabled={testMutation.isPending}
                className="btn-secondary"
              >
                {testMutation.isPending ? 'Testing...' : 'Test'}
              </button>
            </div>

            {testResult && (
              <div className={`p-4 rounded-lg ${
                testResult.success
                  ? 'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800'
                  : 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800'
              }`}>
                <div className="flex items-center gap-2 mb-2">
                  {testResult.success ? (
                    <CheckCircle className="w-5 h-5 text-green-600" />
                  ) : (
                    <XCircle className="w-5 h-5 text-red-600" />
                  )}
                  <span className="font-medium">
                    {testResult.success ? 'Test Passed!' : 'Test Failed'}
                  </span>
                </div>
                <p className="text-sm text-gray-700 dark:text-gray-300">
                  {testResult.output}
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Step 3: Deploy */}
      {generatedAgent && (
        <div className="card p-6">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 font-bold flex items-center justify-center">
              3
            </div>
            <h2 className="text-xl font-semibold">Deploy Agent</h2>
          </div>

          <p className="text-gray-600 dark:text-gray-400 mb-4">
            Your agent is ready to deploy. It will start working automatically once deployed.
          </p>

          <div className="flex gap-3">
            <button
              onClick={() => deployMutation.mutate()}
              disabled={deployMutation.isPending}
              className="btn-primary"
            >
              {deployMutation.isPending ? 'Deploying...' : 'Deploy Agent'}
            </button>
            <button
              onClick={() => {
                setGeneratedAgent(null)
                setDescription('')
                setTestResult(null)
              }}
              className="btn-secondary"
            >
              Start Over
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
