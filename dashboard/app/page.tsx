import { supabase } from '@/lib/supabase'
import { Report } from '@/lib/supabase'

async function getReports(): Promise<Report[]> {
  const { data, error } = await supabase
    .from('reports')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(20)

  if (error) {
    console.error(error)
    return []
  }

  return data || []
}

export default async function Home() {
  const reports = await getReports()

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 p-8">
      <div className="max-w-5xl mx-auto">

        {/* 헤더 */}
        <div className="mb-10">
          <h1 className="text-3xl font-bold text-white">QA-Flow Dashboard</h1>
          <p className="text-zinc-400 mt-1">AI 기반 코드 품질 분석 결과</p>
        </div>

        {/* 통계 카드 */}
        <div className="grid grid-cols-3 gap-4 mb-10">
          <div className="bg-zinc-900 rounded-xl p-5 border border-zinc-800">
            <p className="text-zinc-400 text-sm">총 스캔 횟수</p>
            <p className="text-3xl font-bold text-white mt-1">{reports.length}</p>
          </div>
          <div className="bg-zinc-900 rounded-xl p-5 border border-zinc-800">
            <p className="text-zinc-400 text-sm">위반 발견</p>
            <p className="text-3xl font-bold text-red-400 mt-1">
              {reports.filter(r => r.has_violations).length}
            </p>
          </div>
          <div className="bg-zinc-900 rounded-xl p-5 border border-zinc-800">
            <p className="text-zinc-400 text-sm">정상</p>
            <p className="text-3xl font-bold text-green-400 mt-1">
              {reports.filter(r => !r.has_violations).length}
            </p>
          </div>
        </div>

        {/* 리포트 목록 */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-white">최근 분석 결과</h2>
          {reports.length === 0 ? (
            <div className="bg-zinc-900 rounded-xl p-8 text-center text-zinc-500 border border-zinc-800">
              아직 분석 결과가 없습니다.
            </div>
          ) : (
            reports.map((report) => (
              <div key={report.id} className="bg-zinc-900 rounded-xl p-6 border border-zinc-800">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      report.has_violations
                        ? 'bg-red-900 text-red-300'
                        : 'bg-green-900 text-green-300'
                    }`}>
                      {report.has_violations ? '위반 있음' : '정상'}
                    </span>
                    <span className="text-zinc-400 text-sm">{report.repo}</span>
                    <span className="text-zinc-600 text-sm">{report.branch}</span>
                  </div>
                  <div className="flex items-center gap-2 text-zinc-500 text-sm">
                    <span>{report.provider}</span>
                    <span>·</span>
                    <span>{new Date(report.created_at).toLocaleString('ko-KR')}</span>
                  </div>
                </div>

                {/* AI 리뷰 */}
                {report.ai_review && (
                  <details className="mb-3">
                    <summary className="text-sm text-zinc-400 cursor-pointer hover:text-zinc-200">
                      AI 리뷰 보기
                    </summary>
                    <div className="mt-2 text-sm text-zinc-300 bg-zinc-800 rounded-lg p-4 whitespace-pre-wrap">
                      {report.ai_review}
                    </div>
                  </details>
                )}

                {/* 컨벤션 체크 */}
                {report.convention_check && (
                  <details>
                    <summary className="text-sm text-zinc-400 cursor-pointer hover:text-zinc-200">
                      컨벤션 체크 보기
                    </summary>
                    <div className="mt-2 text-sm text-zinc-300 bg-zinc-800 rounded-lg p-4 whitespace-pre-wrap font-mono">
                      {report.convention_check}
                    </div>
                  </details>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}