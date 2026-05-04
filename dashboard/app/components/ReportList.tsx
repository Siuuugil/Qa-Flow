'use client'

import { useState } from 'react'
import { Report } from '@/lib/supabase'
import ReportCard from './ReportCard'

interface Props {
  reports: Report[]
}

export default function ReportList({ reports }: Props) {
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState<'all' | 'violations' | 'clean'>('all')

  const filtered = reports.filter(report => {
    const matchSearch = report.repo.toLowerCase().includes(search.toLowerCase())
    const matchFilter =
      filter === 'all' ||
      (filter === 'violations' && report.has_violations) ||
      (filter === 'clean' && !report.has_violations)

    return matchSearch && matchFilter
  })

  return (
    <div>
      {/* 검색 + 필터 */}
      <div className="flex gap-3 mb-6">
        <input
          type="text"
          placeholder="레포 이름으로 검색..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="flex-1 bg-zinc-900 border border-zinc-700 rounded-lg px-4 py-2 text-white placeholder-zinc-500 focus:outline-none focus:border-zinc-500"
        />
        <div className="flex gap-2">
          {(['all', 'violations', 'clean'] as const).map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filter === f
                  ? 'bg-zinc-100 text-zinc-900'
                  : 'bg-zinc-900 text-zinc-400 border border-zinc-700 hover:border-zinc-500'
              }`}
            >
              {f === 'all' ? '전체' : f === 'violations' ? '위반 있음' : '정상'}
            </button>
          ))}
        </div>
      </div>

      {/* 결과 수 */}
      <p className="text-zinc-500 text-sm mb-4">
        {filtered.length}개의 결과
      </p>

      {/* 리포트 목록 */}
      <div className="space-y-4">
        {filtered.length === 0 ? (
          <div className="bg-zinc-900 rounded-xl p-8 text-center text-zinc-500 border border-zinc-800">
            검색 결과가 없습니다.
          </div>
        ) : (
          filtered.map(report => (
            <ReportCard key={report.id} report={report} />
          ))
        )}
      </div>
    </div>
  )
}