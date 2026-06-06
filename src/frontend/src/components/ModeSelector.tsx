import type { SolverMode } from '../types'

interface ModeSelectorProps {
  value: SolverMode
  onChange: (mode: SolverMode) => void
  variant?: 'space' | 'warm'
}

const modes: Array<{ value: SolverMode; title: string; description: string }> = [
  {
    value: 'hint',
    title: '思路提示',
    description: '给出 2-3 个关键切入点，不直接交答案。',
  },
  {
    value: 'brief',
    title: '简略思路',
    description: '展示完整步骤，但保持简洁。',
  },
  {
    value: 'detailed',
    title: '详细详解',
    description: '逐步解释原因，并总结知识点。',
  },
]

export function ModeSelector({ value, onChange, variant = 'space' }: ModeSelectorProps) {
  return (
    <div className="grid gap-3 md:grid-cols-3">
      {modes.map((mode) => {
        const active = mode.value === value
        const buttonClass =
          variant === 'warm'
            ? active
              ? 'border-amber-300 bg-amber-50 shadow-lg shadow-amber-100/70'
              : 'border-stone-200 bg-white/70 hover:border-amber-200 hover:bg-amber-50/60'
            : active
              ? 'border-skyline bg-skyline/15 shadow-glow'
              : 'border-white/10 bg-white/5 hover:border-white/25 hover:bg-white/10'
        const titleClass = variant === 'warm' ? 'text-stone-950' : 'text-white'
        const descriptionClass = variant === 'warm' ? 'text-stone-600' : 'text-slate-300'

        return (
          <button
            className={[
              'rounded-2xl border px-4 py-4 text-left transition',
              buttonClass,
            ].join(' ')}
            key={mode.value}
            onClick={() => onChange(mode.value)}
            type="button"
          >
            <div className={`mb-2 text-sm font-semibold ${titleClass}`}>{mode.title}</div>
            <div className={`text-sm ${descriptionClass}`}>{mode.description}</div>
          </button>
        )}
      )}
    </div>
  )
}
