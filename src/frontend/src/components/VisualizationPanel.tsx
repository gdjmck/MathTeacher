import type { PlotResponse, VisualizationHint } from '../types'

interface VisualizationPanelProps {
  hint: VisualizationHint
  plot?: PlotResponse | null
  variant?: 'space' | 'warm'
}

const typeLabels: Record<string, string> = {
  none: '无需图形',
  geometry: '几何图形',
  function_graph: '函数图像',
  coordinate: '坐标系',
  statistics: '统计图表',
  number_line: '数轴',
  vector: '向量图',
}

function getPlotImageSrc(plot?: PlotResponse | null): string | null {
  if (!plot) {
    return null
  }

  if (plot.image_data) {
    return `data:image/png;base64,${plot.image_data}`
  }

  return plot.image_url ?? null
}

export function VisualizationPanel({ hint, plot, variant = 'space' }: VisualizationPanelProps) {
  const imageSrc = getPlotImageSrc(plot)
  const cardClass =
    variant === 'warm'
      ? 'rounded-3xl border border-stone-200/80 bg-white/70 p-5 shadow-lg shadow-stone-200/40'
      : 'rounded-3xl border border-white/10 bg-white/5 p-5'
  const headingClass = variant === 'warm' ? 'text-stone-950' : 'text-white'
  const mutedClass = variant === 'warm' ? 'text-stone-600' : 'text-slate-300'
  const pillClass =
    variant === 'warm'
      ? 'rounded-full border border-stone-200 bg-white/70 px-3 py-1 text-xs text-stone-600'
      : 'rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-200'
  const hintBoxClass =
    variant === 'warm'
      ? 'rounded-2xl border border-dashed border-stone-300 bg-stone-50/80 p-4 text-sm text-stone-600'
      : 'rounded-2xl border border-dashed border-white/10 bg-slate-950/40 p-4 text-sm text-slate-300'
  const imageBoxClass =
    variant === 'warm'
      ? 'mt-4 overflow-hidden rounded-2xl border border-dashed border-amber-200 bg-gradient-to-br from-amber-50 to-stone-50 text-center text-sm text-stone-600'
      : 'mt-4 overflow-hidden rounded-2xl border border-dashed border-skyline/30 bg-gradient-to-br from-skyline/10 to-plum/10 text-center text-sm text-slate-300'

  return (
    <section className={cardClass}>
      <div className="mb-4 flex items-center justify-between gap-4">
        <div>
          <h3 className={`text-lg font-semibold ${headingClass}`}>辅助图</h3>
          <p className={`mt-1 text-sm ${mutedClass}`}>需要画图时，会自动显示在这里。</p>
        </div>
        <span className={pillClass}>
          {typeLabels[hint.type]}
        </span>
      </div>

      <div className={hintBoxClass}>
        <p>{hint.description}</p>
        {hint.keywords.length > 0 ? <p className="mt-3">命中关键词：{hint.keywords.join('、')}</p> : null}
      </div>

      <div className={imageBoxClass}>
        {imageSrc ? (
          <div className="bg-white p-3">
            <img alt="数学辅助图形" className="mx-auto max-h-[460px] w-full object-contain" src={imageSrc} />
          </div>
        ) : (
          <div className="grid min-h-40 place-items-center p-4">
            <div>
              <div className={`font-medium ${headingClass}`}>{hint.needed ? '等待图形结果' : '无需生成图形'}</div>
              <div className="mt-2 max-w-xs">
                {plot?.error
                  ? '暂时没有生成图形，答案仍可正常查看。'
                  : hint.needed
                    ? '正在根据题目内容准备辅助图。'
                    : '这道题主要看文字步骤即可。'}
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  )
}
