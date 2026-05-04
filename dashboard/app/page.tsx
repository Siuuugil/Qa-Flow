import { supabase } from '@/lib/supabase'
import { Report } from '@/lib/supabase'
import ReportList from './components/ReportList'

async function getReports(): Promise<Report[]> {
  const { data, error } = await supabase
    .from('reports')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(50)

  if (error) {
    console.error(error)
    return []
  }

  return data || []
}

export default async function Home() {
  const reports = await getReports()

  const totalScans = reports.length
  const violations = reports.filter(r => r.has_violations).length
  const clean = reports.filter(r => !r.has_violations).length

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
            <p className="text-3xl font-bold text-white mt-1">{totalScans}</p>
          </div>
          <div className="bg-zinc-900 rounded-xl p-5 border border-zinc-800">
            <p className="text-zinc-400 text-sm">위반 발견</p>
            <p className="text-3xl font-bold text-red-400 mt-1">{violations}</p>
          </div>
          <div className="bg-zinc-900 rounded-xl p-5 border border-zinc-800">
            <p className="text-zinc-400 text-sm">정상</p>
            <p className="text-3xl font-bold text-green-400 mt-1">{clean}</p>
          </div>
        </div>

        {/* 리포트 목록 */}
        <div>
          <h2 className="text-xl font-semibold text-white mb-4">최근 분석 결과</h2>
          <ReportList reports={reports} />
        </div>

      </div>
    </div>
  )
}