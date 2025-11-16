import { useQuery } from '@tanstack/react-query'
import { api } from '../../lib/api'
import { Award, Download, ExternalLink } from 'lucide-react'
import { format } from 'date-fns'

export default function Certificates() {
  const { data: certificates } = useQuery({
    queryKey: ['certificates'],
    queryFn: () => api.get('/academy/certificates'),
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          My Certificates
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Your achievements and verifiable credentials
        </p>
      </div>

      {certificates?.data && certificates.data.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {certificates.data.map((cert: any) => (
            <div key={cert.id} className="card p-6 border-2 border-yellow-200 dark:border-yellow-900">
              <div className="flex items-start justify-between mb-4">
                <Award className="w-12 h-12 text-yellow-500" />
                <span className="text-xs text-gray-500">
                  {format(new Date(cert.issued_at), 'MMM dd, yyyy')}
                </span>
              </div>

              <h3 className="font-semibold text-lg text-gray-900 dark:text-white mb-2">
                {cert.title}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                {cert.description}
              </p>

              <div className="flex gap-2">
                <a
                  href={cert.pdf_url}
                  download
                  className="flex-1 btn-primary flex items-center justify-center gap-2"
                >
                  <Download className="w-4 h-4" />
                  Download
                </a>
                <a
                  href={cert.verification_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-secondary flex items-center gap-2"
                >
                  <ExternalLink className="w-4 h-4" />
                </a>
              </div>

              <p className="text-xs text-gray-500 mt-3 text-center">
                ID: {cert.certificate_id}
              </p>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <Award className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500 mb-2">No certificates yet</p>
          <p className="text-sm text-gray-400">
            Complete courses to earn certificates!
          </p>
        </div>
      )}
    </div>
  )
}
