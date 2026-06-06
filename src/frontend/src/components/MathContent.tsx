import { renderMathText } from '../lib/math'

interface MathContentProps {
  content: string
  variant?: 'space' | 'warm'
}

export function MathContent({ content, variant = 'space' }: MathContentProps) {
  const className =
    variant === 'warm'
      ? 'prose max-w-none text-sm leading-7 text-stone-800 prose-p:my-2 prose-strong:text-stone-950'
      : 'prose prose-invert max-w-none text-sm leading-7 text-slate-200 prose-p:my-2 prose-strong:text-white'

  return (
    <div className={className}>
      {renderMathText(content)}
    </div>
  )
}
