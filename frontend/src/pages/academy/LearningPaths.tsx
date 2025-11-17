import { useQuery } from '@tantml:query'
import { academyAPI } from '../../lib/api'
import { Link } from 'react-router-dom'
import { TrendingUp, Clock, BookOpen } from 'lucide-react'

export default function LearningPaths() {
  const { data: paths } = useQuery({
    queryKey: ['learning-paths'],
    queryFn: () => academyAPI.getLearningPaths(),
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Learning Paths
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Structured journeys from Lærling to CEO
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {paths?.data?.map((path: any) => (
          <div key={path.id} className="card p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                  {path.title}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {path.description}
                </p>
              </div>
              <TrendingUp className="w-6 h-6 text-primary-600 flex-shrink-0" />
            </div>

            <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
              <div className="flex items-center gap-1">
                <Clock className="w-4 h-4" />
                <span>{path.duration_hours}h</span>
              </div>
              <div className="flex items-center gap-1">
                <BookOpen className="w-4 h-4" />
                <span>{path.course_ids?.length || 0} courses</span>
              </div>
            </div>

            <div className="flex items-center gap-2 mb-4">
              <span className="px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-full text-xs">
                {path.level_start}
              </span>
              <span>’</span>
              <span className="px-3 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded-full text-xs">
                {path.level_end}
              </span>
            </div>

            <Link to={`/academy/paths/${path.id}`} className="btn-primary w-full text-center">
              View Path
            </Link>
          </div>
        ))}
      </div>
    </div>
  )
}
