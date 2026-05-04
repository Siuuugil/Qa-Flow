import { supabase } from '@/lib/supabase'
import { Report } from '@/lib/supabase'
import Link from 'next/link'

async function getReport(id: string): Promise<Report | null> {
  const { data, error } = await supabase
    .from('reports')
    .select('*')
    .eq('id', id)
    .single()

  if (error) return null
  return data
}

export default async function ReportDetail({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const report = await getReport(id)

  if (!report) {
    return (
      <div className="min-h-screen bg-zinc-950 text-zinc-100 p-8">
        <div className="max-w-4xl mx-auto">
          <p className="text-zinc-400">리포트를 찾을 수 없습니다.</p>
          <Link href="/" className="text-zinc-400 hover:text-white mt-4 inline-block">
            돌아가기
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 p-8">
      <div className="max-w-4xl mx-auto">

        {/* 뒤로가기 */}
        <Link href="/" className="text-zinc-400 hover:text-white text-sm mb-6 inline-block">
          ← 목록으로
        </Link>

        {/* 헤더 */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
              report.has_violations
                ? 'bg-red-900 text-red-300'
                : 'bg-green-900 text-green-300'
            }`}>
              {report.has_violations ? '위반 있음' : '정상'}
            </span>
            <h1 className="text-2xl font-bold text-white">{report.repo}</h1>
          </div>
          <div className="flex gap-4 text-zinc-500 text-sm">
            <span>브랜치: {report.branch}</span>
            <span>Provider: {report.provider}</span>
            <span>Focus: {report.focus || 'general'}</span>
            <span>Mode: {report.mode}</span>
            <span suppressHydrationWarning>
              {new Date(report.created_at).toLocaleString('ko-KR')}
            </span>
          </div>
        </div>

        {/* 컨벤션 체크 */}
        <div className="bg-zinc-900 rounded-xl p-6 border border-zinc-800 mb-6">
          <h2 className="text-lg font-semibold text-white mb-4">컨벤션 체크</h2>
          <pre className="text-sm text-zinc-300 whitespace-pre-wrap font-mono">
            {report.convention_check || '컨벤션 체크 결과 없음'}
          </pre>
        </div>

        {/* AI 리뷰 */}
        <div className="bg-zinc-900 rounded-xl p-6 border border-zinc-800">
          <h2 className="text-lg font-semibold text-white mb-4">AI 코드 리뷰</h2>
          <div className="text-sm text-zinc-300 whitespace-pre-wrap">
            {report.ai_review || 'AI 리뷰 결과 없음'}
          </div>
        </div>

      </div>
    </div>
  )
}