import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery, useMutation } from '@tanstack/react-query'
import { academyAPI } from '../../lib/api'
import { MessageSquare, ChevronLeft, ChevronRight, CheckCircle, Circle, Bot } from 'lucide-react'
import toast from 'react-hot-toast'

export default function CoursePlayer() {
  const { courseId } = useParams()
  const [currentLessonIndex, setCurrentLessonIndex] = useState(0)
  const [showAIAssistant, setShowAIAssistant] = useState(false)
  const [aiQuestion, setAiQuestion] = useState('')
  const [aiMessages, setAiMessages] = useState<any[]>([])

  const { data: course } = useQuery({
    queryKey: ['course', courseId],
    queryFn: () => academyAPI.getCourse(courseId!),
  })

  const askAIMutation = useMutation({
    mutationFn: (question: string) => academyAPI.askAssistant(question, courseId!),
    onSuccess: (response) => {
      setAiMessages((prev) => [
        ...prev,
        {
          role: 'user',
          content: aiQuestion,
        },
        {
          role: 'assistant',
          content: response.data.message,
          suggested_actions: response.data.suggested_actions,
        },
      ])
      setAiQuestion('')
    },
  })

  const handleAskAI = (e: React.FormEvent) => {
    e.preventDefault()
    if (!aiQuestion.trim()) return
    askAIMutation.mutate(aiQuestion)
  }

  const currentModule = course?.data?.modules?.[0] // Simplified for now
  const currentLesson = currentModule?.lessons?.[currentLessonIndex]

  const goToNextLesson = () => {
    if (currentLessonIndex < (currentModule?.lessons?.length || 0) - 1) {
      setCurrentLessonIndex(currentLessonIndex + 1)
    }
  }

  const goToPreviousLesson = () => {
    if (currentLessonIndex > 0) {
      setCurrentLessonIndex(currentLessonIndex - 1)
    }
  }

  const renderLessonContent = () => {
    if (!currentLesson) return null

    switch (currentLesson.lesson_type) {
      case 'video':
        return (
          <div className="aspect-video bg-gray-900 rounded-lg flex items-center justify-center">
            <video
              src={currentLesson.content?.video_url}
              controls
              className="w-full h-full rounded-lg"
            />
          </div>
        )

      case 'text':
        return (
          <div className="prose dark:prose-invert max-w-none">
            <div dangerouslySetInnerHTML={{ __html: currentLesson.content?.markdown || '' }} />
          </div>
        )

      case 'quiz':
        return (
          <div className="space-y-6">
            <h3 className="text-xl font-semibold">Quiz Time! =Ý</h3>
            {currentLesson.content?.questions?.map((q: any, idx: number) => (
              <div key={idx} className="card p-6">
                <p className="font-medium mb-4">{q.question}</p>
                <div className="space-y-2">
                  {q.options?.map((option: string, optIdx: number) => (
                    <button
                      key={optIdx}
                      className="w-full text-left p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors"
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )

      case 'ai_guided':
        return (
          <div className="card p-8 text-center">
            <Bot className="w-16 h-16 text-primary-600 mx-auto mb-4" />
            <h3 className="text-2xl font-bold mb-4">{currentLesson.title}</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              {currentLesson.content?.prompt}
            </p>
            <button
              onClick={() => setShowAIAssistant(true)}
              className="btn-primary"
            >
              Start AI-Guided Lesson
            </button>
          </div>
        )

      case 'project':
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold">{currentLesson.content?.project_title}</h3>
            <p className="text-gray-600 dark:text-gray-400">
              {currentLesson.content?.description}
            </p>
            <div className="card p-6">
              <h4 className="font-semibold mb-3">Steps:</h4>
              <ol className="list-decimal list-inside space-y-2">
                {currentLesson.content?.steps?.map((step: string, idx: number) => (
                  <li key={idx} className="text-gray-700 dark:text-gray-300">
                    {step}
                  </li>
                ))}
              </ol>
            </div>
          </div>
        )

      default:
        return (
          <div className="card p-8 text-center">
            <p className="text-gray-500">Lesson content coming soon...</p>
          </div>
        )
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[calc(100vh-120px)]">
      {/* Sidebar - Lesson List */}
      <div className="lg:col-span-1 card p-4 overflow-y-auto">
        <h3 className="font-semibold mb-4">{course?.data?.title}</h3>
        <div className="space-y-2">
          {currentModule?.lessons?.map((lesson: any, index: number) => (
            <button
              key={index}
              onClick={() => setCurrentLessonIndex(index)}
              className={`w-full text-left p-3 rounded-lg transition-colors ${
                index === currentLessonIndex
                  ? 'bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300'
                  : 'hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <div className="flex items-center gap-2">
                {lesson.completed ? (
                  <CheckCircle className="w-4 h-4 text-green-500" />
                ) : (
                  <Circle className="w-4 h-4 text-gray-400" />
                )}
                <span className="text-sm font-medium truncate">{lesson.title}</span>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                {lesson.lesson_type} · {lesson.duration_minutes}min
              </p>
            </button>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className="lg:col-span-3 space-y-4 overflow-y-auto">
        {/* Lesson Header */}
        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                {currentLesson?.title}
              </h2>
              <p className="text-sm text-gray-500 mt-1">
                {currentLesson?.lesson_type} · {currentLesson?.duration_minutes} minutes
              </p>
            </div>
            <button
              onClick={() => setShowAIAssistant(!showAIAssistant)}
              className="btn-secondary flex items-center gap-2"
            >
              <MessageSquare className="w-4 h-4" />
              AI Assistant
            </button>
          </div>
        </div>

        {/* Lesson Content */}
        <div className="card p-6">
          {renderLessonContent()}
        </div>

        {/* Navigation */}
        <div className="card p-4 flex items-center justify-between">
          <button
            onClick={goToPreviousLesson}
            disabled={currentLessonIndex === 0}
            className="btn-secondary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronLeft className="w-4 h-4" />
            Previous
          </button>

          <span className="text-sm text-gray-500">
            Lesson {currentLessonIndex + 1} of {currentModule?.lessons?.length || 0}
          </span>

          <button
            onClick={goToNextLesson}
            disabled={currentLessonIndex === (currentModule?.lessons?.length || 0) - 1}
            className="btn-primary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        {/* AI Assistant Panel */}
        {showAIAssistant && (
          <div className="card p-6">
            <div className="flex items-center gap-2 mb-4">
              <Bot className="w-6 h-6 text-primary-600" />
              <h3 className="text-lg font-semibold">AI Course Assistant</h3>
            </div>

            {/* Messages */}
            <div className="space-y-4 mb-4 max-h-64 overflow-y-auto">
              {aiMessages.length === 0 ? (
                <p className="text-gray-500 text-center py-4">
                  Ask me anything about this lesson! =

                </p>
              ) : (
                aiMessages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`p-3 rounded-lg ${
                      msg.role === 'user'
                        ? 'bg-primary-50 dark:bg-primary-900/30 ml-8'
                        : 'bg-gray-100 dark:bg-gray-700 mr-8'
                    }`}
                  >
                    <p className="text-sm">{msg.content}</p>
                    {msg.suggested_actions && (
                      <div className="mt-2 flex flex-wrap gap-2">
                        {msg.suggested_actions.map((action: string, i: number) => (
                          <button
                            key={i}
                            onClick={() => setAiQuestion(action)}
                            className="text-xs px-2 py-1 bg-white dark:bg-gray-800 rounded border border-gray-300 dark:border-gray-600 hover:border-primary-500"
                          >
                            {action}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>

            {/* Input */}
            <form onSubmit={handleAskAI} className="flex gap-2">
              <input
                type="text"
                value={aiQuestion}
                onChange={(e) => setAiQuestion(e.target.value)}
                placeholder="Ask a question..."
                className="flex-1 input"
                disabled={askAIMutation.isPending}
              />
              <button
                type="submit"
                disabled={askAIMutation.isPending || !aiQuestion.trim()}
                className="btn-primary"
              >
                {askAIMutation.isPending ? 'Sending...' : 'Ask'}
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  )
}
