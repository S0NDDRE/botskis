import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { academyAPI } from '../../lib/api'
import { Link } from 'react-router-dom'
import { Clock, Award, BookOpen, Filter } from 'lucide-react'
import toast from 'react-hot-toast'

const LEVELS = ['laerling', 'junior', 'medior', 'senior', 'lead', 'manager', 'director', 'ceo']
const CATEGORIES = ['platform_basics', 'ai_agent_builder', 'voice_ai', 'meta_ai_guardian', 'automation', 'business']

export default function CourseList() {
  const [selectedLevel, setSelectedLevel] = useState<string>('')
  const [selectedCategory, setSelectedCategory] = useState<string>('')

  const { data: courses, isLoading } = useQuery({
    queryKey: ['courses', selectedLevel, selectedCategory],
    queryFn: () => academyAPI.getCourses(selectedLevel, selectedCategory),
  })

  const handleEnroll = async (courseId: string) => {
    try {
      await academyAPI.enrollInCourse(courseId)
      toast.success('Enrolled successfully!')
    } catch (error) {
      toast.error('Enrollment failed')
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          All Courses
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Browse and enroll in courses to level up your Mindframe skills
        </p>
      </div>

      {/* Filters */}
      <div className="card p-4">
        <div className="flex items-center gap-4 flex-wrap">
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-gray-500" />
            <span className="font-medium">Filters:</span>
          </div>

          <select
            value={selectedLevel}
            onChange={(e) => setSelectedLevel(e.target.value)}
            className="input max-w-xs"
          >
            <option value="">All Levels</option>
            {LEVELS.map((level) => (
              <option key={level} value={level}>
                {level.charAt(0).toUpperCase() + level.slice(1)}
              </option>
            ))}
          </select>

          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="input max-w-xs"
          >
            <option value="">All Categories</option>
            {CATEGORIES.map((category) => (
              <option key={category} value={category}>
                {category.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Course Grid */}
      {isLoading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="text-gray-500 mt-4">Loading courses...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses?.data?.map((course: any) => (
            <div
              key={course.id}
              className="card p-6 hover:shadow-lg transition-shadow"
            >
              {/* Course Badge */}
              <div className="flex items-center justify-between mb-4">
                <span className="px-3 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 rounded-full text-xs font-medium">
                  {course.level}
                </span>
                {course.is_premium && (
                  <span className="px-3 py-1 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 rounded-full text-xs font-medium">
                    Premium
                  </span>
                )}
              </div>

              {/* Course Info */}
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                {course.title}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
                {course.description}
              </p>

              {/* Course Meta */}
              <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400 mb-4">
                <div className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  <span>{course.duration_minutes}min</span>
                </div>
                <div className="flex items-center gap-1">
                  <BookOpen className="w-4 h-4" />
                  <span>{course.modules_count || 0} modules</span>
                </div>
                {course.awards_certificate && (
                  <div className="flex items-center gap-1">
                    <Award className="w-4 h-4 text-yellow-500" />
                  </div>
                )}
              </div>

              {/* Actions */}
              <div className="flex gap-2">
                <Link
                  to={`/academy/courses/${course.id}`}
                  className="flex-1 btn-primary text-center"
                >
                  View Course
                </Link>
                {!course.is_enrolled && (
                  <button
                    onClick={() => handleEnroll(course.id)}
                    className="btn-secondary"
                  >
                    Enroll
                  </button>
                )}
              </div>
            </div>
          ))}

          {courses?.data?.length === 0 && (
            <div className="col-span-3 text-center py-12">
              <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">No courses found</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
