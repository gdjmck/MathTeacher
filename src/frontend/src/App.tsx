import { useState } from 'react'
import { MathContent } from './components/MathContent'
import { ModeSelector } from './components/ModeSelector'
import { VisualizationPanel } from './components/VisualizationPanel'
import { solveImageProblem, solveTextProblem } from './lib/api'
import type { SolveResponse, SolverMode } from './types'

const modeLabels: Record<SolverMode, string> = {
  hint: '思路提示',
  brief: '简略思路',
  detailed: '详细详解',
}

const sampleQuestions = [
  '求解方程：$3x - 7 = 11$',
  '已知抛物线 $y=x^2-4x+3$，求顶点坐标并判断开口方向。',
  '在直角三角形中，两直角边分别为 3 和 4，求斜边长度。',
]

function App() {
  const [question, setQuestion] = useState(sampleQuestions[0])
  const [mode, setMode] = useState<SolverMode>('hint')
  const [response, setResponse] = useState<SolveResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [sampleIndex, setSampleIndex] = useState(0)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const completed = Boolean(response) && !loading

  const pageClass = completed
    ? 'min-h-screen bg-[radial-gradient(circle_at_top,_rgba(251,191,36,0.18),_transparent_34%),linear-gradient(180deg,#fffaf0_0%,#f7efe6_55%,#eadfce_100%)] text-stone-950 transition-colors duration-700'
    : 'min-h-screen bg-[radial-gradient(circle_at_top,_rgba(59,130,246,0.2),_transparent_35%),linear-gradient(180deg,#020617_0%,#0f172a_55%,#111827_100%)] text-white transition-colors duration-700'
  const heroClass = completed
    ? 'overflow-hidden rounded-[32px] border border-stone-200/80 bg-white/70 shadow-2xl shadow-stone-300/30 backdrop-blur'
    : 'overflow-hidden rounded-[32px] border border-white/10 bg-white/5 shadow-2xl shadow-slate-950/40 backdrop-blur'
  const cardClass = completed
    ? 'rounded-3xl border border-stone-200/80 bg-white/70 p-5 shadow-lg shadow-stone-200/40'
    : 'rounded-3xl border border-white/10 bg-white/5 p-5'
  const innerPanelClass = completed
    ? 'rounded-3xl border border-stone-200/80 bg-stone-50/80 p-5'
    : 'rounded-3xl border border-white/10 bg-slate-950/40 p-5'
  const subtlePanelClass = completed
    ? 'rounded-2xl border border-stone-200/80 bg-white/70 px-4 py-3 text-sm text-stone-700'
    : 'rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-200'
  const dashedPanelClass = completed
    ? 'mt-4 rounded-2xl border border-dashed border-stone-300 bg-stone-50/80 p-4'
    : 'mt-4 rounded-2xl border border-dashed border-white/10 bg-slate-950/30 p-4'
  const selectedFileClass = completed
    ? 'mt-3 flex flex-col gap-3 rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-stone-800 sm:flex-row sm:items-center sm:justify-between'
    : 'mt-3 flex flex-col gap-3 rounded-2xl border border-skyline/20 bg-skyline/10 px-4 py-3 text-sm text-slate-100 sm:flex-row sm:items-center sm:justify-between'
  const textareaClass = completed
    ? 'min-h-52 w-full rounded-2xl border border-stone-200 bg-white/90 px-4 py-4 text-sm leading-7 text-stone-900 outline-none transition placeholder:text-stone-400 focus:border-amber-400 focus:ring-2 focus:ring-amber-200'
    : 'min-h-52 w-full rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-4 text-sm leading-7 text-slate-100 outline-none transition placeholder:text-slate-500 focus:border-skyline focus:ring-2 focus:ring-skyline/30'
  const headingText = completed ? 'text-stone-950' : 'text-white'
  const mutedText = completed ? 'text-stone-600' : 'text-slate-300'
  const softText = completed ? 'text-stone-700' : 'text-slate-200'
  const quietText = completed ? 'text-stone-500' : 'text-slate-400'
  const pillClass = completed
    ? 'rounded-full border border-stone-200 bg-white/70 px-3 py-1 text-xs text-stone-600'
    : 'rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-200'
  const tagClass = completed
    ? 'rounded-full border border-stone-200 bg-white/70 px-3 py-1'
    : 'rounded-full border border-white/10 bg-white/5 px-3 py-1'
  const secondaryButtonClass = completed
    ? 'rounded-full border border-stone-200 bg-white/70 px-3 py-1 text-xs text-stone-600 transition hover:bg-stone-50'
    : 'rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-200 transition hover:bg-white/10'
  const fileButtonClass = completed
    ? 'inline-flex cursor-pointer items-center justify-center rounded-2xl border border-stone-200 bg-white/80 px-4 py-2 text-sm text-stone-700 transition hover:bg-stone-50'
    : 'inline-flex cursor-pointer items-center justify-center rounded-2xl border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-200 transition hover:bg-white/10'
  const removeButtonClass = completed
    ? 'rounded-xl border border-stone-200 bg-white/80 px-3 py-2 text-xs text-stone-700 transition hover:bg-stone-50'
    : 'rounded-xl border border-white/10 bg-white/10 px-3 py-2 text-xs text-white transition hover:bg-white/15'
  const resultBodyClass = completed
    ? 'rounded-2xl border border-stone-200 bg-white/80 p-4'
    : 'rounded-2xl border border-white/10 bg-slate-950/40 p-4'
  const emptyStateClass = completed
    ? 'grid min-h-72 place-items-center rounded-2xl border border-dashed border-stone-300 bg-stone-50/70 text-center text-sm text-stone-500'
    : 'grid min-h-72 place-items-center rounded-2xl border border-dashed border-white/10 bg-slate-950/30 text-center text-sm text-slate-400'

  function handleUseNextSample() {
    const nextIndex = (sampleIndex + 1) % sampleQuestions.length
    setSampleIndex(nextIndex)
    setQuestion(sampleQuestions[nextIndex])
  }

  async function handleSolve() {
    const trimmedQuestion = question.trim()
    if (!selectedFile && !trimmedQuestion) {
      setError('请输入题目后再开始解答。')
      return
    }

    setLoading(true)
    setError(null)
    setResponse(null)

    try {
      const result = selectedFile
        ? await solveImageProblem(selectedFile, mode)
        : await solveTextProblem({ question: trimmedQuestion, mode, generate_plot: true })
      setResponse(result)
    } catch (solveError) {
      const message = solveError instanceof Error ? solveError.message : '解题失败'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={pageClass}>
      <main className="mx-auto flex w-full max-w-7xl flex-col gap-8 px-4 py-8 sm:px-6 lg:px-8">
        <section className={heroClass}>
          <div className="grid gap-8 px-6 py-8 lg:grid-cols-[1.15fr_0.85fr] lg:px-8">
            <div>
              <div className={completed ? 'inline-flex rounded-full border border-amber-200 bg-amber-50 px-3 py-1 text-xs font-medium uppercase tracking-[0.2em] text-amber-700' : 'inline-flex rounded-full border border-skyline/30 bg-skyline/10 px-3 py-1 text-xs font-medium uppercase tracking-[0.2em] text-sky-200'}>
                Math Tutor
              </div>
              <h1 className={`mt-4 max-w-2xl font-display text-4xl font-semibold tracking-tight sm:text-5xl ${headingText}`}>
                拍题或输入，获得清晰讲解
              </h1>
              <p className={`mt-4 max-w-2xl text-base leading-7 ${mutedText}`}>
                选择你需要的讲解深度，必要时会自动配一张辅助图。
              </p>
              <div className={`mt-6 flex flex-wrap gap-3 text-sm ${softText}`}>
                <span className={tagClass}>思路提示</span>
                <span className={tagClass}>完整步骤</span>
                <span className={tagClass}>详细讲解</span>
                <span className={tagClass}>辅助图形</span>
              </div>
            </div>

            <div className={innerPanelClass}>
              <div className={`text-sm ${mutedText}`}>使用方式</div>
              <div className={`mt-3 space-y-3 text-sm leading-6 ${softText}`}>
                <p>1. 输入题目，或上传题目图片。</p>
                <p>2. 选择讲解方式。</p>
                <p>3. 查看答案和辅助图。</p>
              </div>
            </div>
          </div>
        </section>

        <section className={cardClass}>
          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <h2 className={`text-xl font-semibold ${headingText}`}>选择模式</h2>
            <div className="lg:min-w-[560px]">
              <ModeSelector onChange={setMode} value={mode} variant={completed ? 'warm' : 'space'} />
            </div>
          </div>
        </section>

        <section className="grid gap-6 lg:grid-cols-[1fr_1.05fr]">
          <div className="space-y-6">
            <section className={cardClass}>
              <div className="mb-4 flex items-center justify-between gap-4">
                <div>
                  <h2 className={`text-xl font-semibold ${headingText}`}>输入题目</h2>
                  <p className={`mt-1 text-sm ${mutedText}`}>可以直接输入，也可以上传图片。</p>
                </div>
                <button
                  className={secondaryButtonClass}
                  onClick={handleUseNextSample}
                  type="button"
                >
                  切换示例
                </button>
              </div>

              <textarea
                className={textareaClass}
                onChange={(event) => setQuestion(event.target.value)}
                placeholder="例如：求解方程 $2x + 5 = 15$，并说明为什么这样变形。"
                value={question}
              />

              <div className={dashedPanelClass}>
                <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <div className={`text-sm font-medium ${headingText}`}>图片上传</div>
                    <div className={`mt-1 text-xs ${quietText}`}>适合手机拍下来的题目。</div>
                  </div>
                  <label className={fileButtonClass}>
                    选择文件
                    <input
                      accept="image/*,.txt"
                      className="hidden"
                      onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)}
                      type="file"
                    />
                  </label>
                </div>

                {selectedFile ? (
                  <div className={selectedFileClass}>
                    <div>
                      已选择文件：{selectedFile.name}
                      <div className={`mt-1 text-xs ${mutedText}`}>将优先识别图片中的题目。</div>
                    </div>
                    <button
                      className={removeButtonClass}
                      onClick={() => setSelectedFile(null)}
                      type="button"
                    >
                      移除文件
                    </button>
                  </div>
                ) : null}
              </div>

              <div className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div className={`text-sm ${mutedText}`}>当前模式：{modeLabels[mode]}</div>
                <button
                  className="inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-skyline to-plum px-5 py-3 text-sm font-medium text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
                  disabled={loading}
                  onClick={handleSolve}
                  type="button"
                >
                  {loading ? '正在生成答案...' : '开始解题'}
                </button>
              </div>

              {error ? <div className="mt-4 rounded-2xl border border-rose-400/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-700">{error}</div> : null}
            </section>
          </div>

          <div className="space-y-6">
            <section className={cardClass}>
              <div className="mb-4 flex items-center justify-between gap-4">
                <div>
                  <h2 className={`text-xl font-semibold ${headingText}`}>解题结果</h2>
                  <p className={`mt-1 text-sm ${mutedText}`}>重点步骤和公式会在这里显示。</p>
                </div>
                <span className={pillClass}>
                  {modeLabels[mode]}
                </span>
              </div>

              {response ? (
                <div className={resultBodyClass}>
                  <div className={`mb-4 flex flex-wrap items-center gap-2 text-xs ${quietText}`}>
                    <span className={pillClass}>来源：{response.source === 'image' ? '图片/文件' : '文本'}</span>
                    {response.extracted_text ? <span className={pillClass}>已识别题目</span> : null}
                  </div>
                  {response.extracted_text ? (
                    <div className={subtlePanelClass}>
                      <div className={`mb-2 text-xs uppercase tracking-[0.2em] ${quietText}`}>提取到的题目</div>
                      <div>{response.extracted_text}</div>
                    </div>
                  ) : null}
                  <div className={`mb-4 text-xs uppercase tracking-[0.2em] ${quietText}`}>回答内容</div>
                  <MathContent content={response.content} variant={completed ? 'warm' : 'space'} />
                </div>
              ) : (
                <div className={emptyStateClass}>
                  <div>
                    <div className={`text-base font-medium ${softText}`}>{loading ? '正在思考' : '等待输入题目'}</div>
                    <div className="mt-2 max-w-sm">点击“开始解题”后，这里会展示讲解内容。</div>
                  </div>
                </div>
              )}
            </section>

            <VisualizationPanel
              hint={
                response?.visualization_hint ?? {
                  needed: false,
                  type: 'none',
                  description: '需要图形辅助时，会自动生成。',
                  keywords: [],
                }
              }
              plot={response?.plot ?? null}
              variant={completed ? 'warm' : 'space'}
            />
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
