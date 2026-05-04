import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

export type Report = {
  id: string
  created_at: string
  repo: string
  branch: string
  provider: string
  focus: string
  mode: string
  ai_review: string
  convention_check: string
  has_violations: boolean
}