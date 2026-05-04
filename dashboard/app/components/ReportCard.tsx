'use client'

import { Report } from '@/lib/supabase'
import { useRouter } from 'next/navigation'

interface Props {
  report: Report
}

export default function ReportCard({ report }: Props) {
  const router = useRouter()

  return (
    <div
      onClick={() => router.push(`/reports/${report.id}`)}
      className="bg-zinc-900 rounded-xl p-6 border border-zinc-800 hover:border-zinc-600 transition-colors cursor-pointer"
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
            report.has_violations
              ? 'bg-red-900 text-red-300'
              : 'bg-green-900 text-green-300'
          }`}>
            {report.has_violations ? '위반 있음' : '정상'}
          </span>
          <span className="text-white font-medium">{report.repo}</span>
          <span className="text-zinc-500 text-sm">{report.branch}</span>
        </div>
        <div className="flex items-center gap-2 text-zinc-500 text-sm">
          <span className="px-2 py-1 bg-zinc-800 rounded text-zinc-400 text-xs">
            {report.focus || 'general'}
          </span>
          <span>{report.provider}</span>
          <span>·</span>
          <span suppressHydrationWarning>
            {new Date(report.created_at).toLocaleString('ko-KR')}
          </span>
        </div>
      </div>

      {report.ai_review && (
        <details className="mb-3" onClick={e => e.stopPropagation()}>
          <summary className="text-sm text-zinc-400 cursor-pointer hover:text-zinc-200">
            AI 리뷰 보기
          </summary>
          <div className="mt-2 text-sm text-zinc-300 bg-zinc-800 rounded-lg p-4 whitespace-pre-wrap">
            {report.ai_review}
          </div>
        </details>
      )}

      {report.convention_check && (
        <details onClick={e => e.stopPropagation()}>
          <summary className="text-sm text-zinc-400 cursor-pointer hover:text-zinc-200">
            컨벤션 체크 보기
          </summary>
          <div className="mt-2 text-sm text-zinc-300 bg-zinc-800 rounded-lg p-4 whitespace-pre-wrap font-mono">
            {report.convention_check}
          </div>
        </details>
      )}
    </div>
  )
}