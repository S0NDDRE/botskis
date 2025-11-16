import { useQuery } from '@tanstack/react-query'
import { academyAPI } from '../../lib/api'
import { Link } from 'react-router-dom'
import { BookOpen, Clock, TrendingUp } from 'lucide-react'

export default function MyCourses() {
  const { data: courses } = useQuery({
    queryKey: ['my-courses'],
    queryFn: () => academyAPI.getMyCourses(),
  })

  const inProgress = courses?.data?.filter((c: any) => c.progress > 0 && c.progress < 100) || []
  const completed = courses?.data?.filter((c: any) => c.progress === 100) || []

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          My Courses
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Track your learning progress
        </p>
      </div>

      {/* In Progress */}
      <div>
        <h2 className="text-xl font-semibold mb-4">In Progress</h2>
        {inProgress.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {inProgress.map((course: any) => (
              <Link
                key={course.id}
                to={`/academy/courses/${course.id}`}
                className="card p-6 hover:shadow-lg transition-shadow"
              >
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                  {course.title}
                </h3>
                <div className="flex items-center gap-2 text-sm text-gray-500 mb-4">
                  <Clock className="w-4 h-4" />
                  <span>{course.duration_minutes}min</span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div
                    className="bg-primary-600 h-2 rounded-full transition-all"
                    style={{ width: `${course.progress}%` }}
                  />
                </div>
                <p className="text-sm text-gray-500 mt-2">{course.progress}% complete</p>
              </Link>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">No courses in progress</p>
        )}
      </div>

      {/* Completed */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Completed</h2>
        {completed.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {completed.map((course: any) => (
              <div key={course.id} className="card p-6">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                  {course.title}
                </h3>
                <div className="flex items-center gap-2 text-sm text-green-600">
                  <TrendingUp className="w-4 h-4" />
                  <span>Completed!</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">No completed courses yet</p>
        )}
      </div>
    </div>
  )
}
