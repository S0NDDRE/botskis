import { useQuery } from '@tanstack/react-query'
import { academyAPI } from '../../lib/api'
import { GraduationCap, BookOpen, Award, TrendingUp, Clock, Target } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function AcademyDashboard() {
  const { data: progress } = useQuery({
    queryKey: ['academy-progress'],
    queryFn: () => academyAPI.getProgress(),
  })

  const { data: myCourses } = useQuery({
    queryKey: ['my-courses'],
    queryFn: () => academyAPI.getMyCourses(),
  })

  const stats = [
    {
      name: 'Courses Enrolled',
      value: myCourses?.data?.length || 0,
      icon: BookOpen,
      color: 'bg-blue-500'
    },
    {
      name: 'Certificates',
      value: progress?.data?.certificates_earned || 0,
      icon: Award,
      color: 'bg-yellow-500'
    },
    {
      name: 'Learning Streak',
      value: `${progress?.data?.streak_days || 0} days`,
      icon: TrendingUp,
      color: 'bg-green-500'
    },
    {
      name: 'Time Spent',
      value: `${progress?.data?.total_time_minutes || 0}min`,
      icon: Clock,
      color: 'bg-purple-500'
    }
  ]

  const currentLevel = progress?.data?.current_level || 'laerling'
  const levelNames: Record<string, string> = {
    laerling: 'Lærling (Apprentice)',
    junior: 'Junior',
    medior: 'Medior',
    senior: 'Senior',
    lead: 'Lead',
    manager: 'Manager',
    director: 'Director',
    ceo: 'CEO'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Mindframe Academy <“
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Your journey from Lærling to CEO
          </p>
        </div>
        <Link to="/academy/courses" className="btn-primary">
          Browse Courses
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.name} className="card p-6">
            <div className="flex items-center gap-4">
              <div className={`${stat.color} p-3 rounded-lg text-white`}>
                <stat.icon className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stat.value}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Current Level */}
      <div className="card p-6">
        <div className="flex items-center gap-4 mb-4">
          <Target className="w-6 h-6 text-primary-600" />
          <h2 className="text-xl font-semibold">Your Current Level</h2>
        </div>
        <div className="flex items-center gap-6">
          <div className="flex-shrink-0">
            <div className="w-20 h-20 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white font-bold text-2xl">
              {currentLevel[0].toUpperCase()}
            </div>
          </div>
          <div className="flex-1">
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              {levelNames[currentLevel]}
            </h3>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
              <div
                className="bg-gradient-to-r from-primary-500 to-primary-600 h-3 rounded-full transition-all duration-500"
                style={{ width: `${progress?.data?.level_progress || 0}%` }}
              />
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
              {progress?.data?.level_progress || 0}% to next level
            </p>
          </div>
        </div>
      </div>

      {/* Continue Learning */}
      {myCourses?.data && myCourses.data.length > 0 && (
        <div className="card p-6">
          <h2 className="text-xl font-semibold mb-4">Continue Learning</h2>
          <div className="space-y-4">
            {myCourses.data.slice(0, 3).map((course: any) => (
              <Link
                key={course.id}
                to={`/academy/courses/${course.id}`}
                className="flex items-center gap-4 p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-primary-500 hover:shadow-md transition-all"
              >
                <div className="flex-shrink-0">
                  <GraduationCap className="w-10 h-10 text-primary-600" />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-gray-900 dark:text-white truncate">
                    {course.title}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {course.level} · {course.duration_minutes}min
                  </p>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-2">
                    <div
                      className="bg-primary-600 h-2 rounded-full"
                      style={{ width: `${course.progress || 0}%` }}
                    />
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Recommended Courses */}
      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-4">Recommended for You</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {progress?.data?.recommended_courses?.map((course: any) => (
            <Link
              key={course.id}
              to={`/academy/courses/${course.id}`}
              className="p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-primary-500 hover:shadow-md transition-all"
            >
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                {course.title}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                {course.description}
              </p>
              <div className="flex items-center justify-between text-sm">
                <span className="text-primary-600">{course.level}</span>
                <span className="text-gray-500">{course.duration_minutes}min</span>
              </div>
            </Link>
          )) || (
            <p className="col-span-3 text-center text-gray-500 py-8">
              Complete more courses to get recommendations
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
