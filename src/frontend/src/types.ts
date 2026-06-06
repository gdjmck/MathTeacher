export type SolverMode = 'hint' | 'brief' | 'detailed'

export type VisualizationType =
  | 'none'
  | 'geometry'
  | 'function_graph'
  | 'coordinate'
  | 'statistics'
  | 'number_line'
  | 'vector'

export interface SolveRequest {
  question: string
  mode: SolverMode
  generate_plot?: boolean
}

export interface VisualizationHint {
  needed: boolean
  type: VisualizationType
  description: string
  keywords: string[]
}

export interface PlotResponse {
  success: boolean
  method: 'gpt_image2' | 'matplotlib' | 'none' | string
  image_data?: string | null
  image_url?: string | null
  code?: string | null
  error?: string | null
}

export interface SolveResponse {
  mode: SolverMode
  content: string
  question: string
  needs_visualization: boolean
  visualization_hint: VisualizationHint
  source: 'text' | 'image'
  extracted_text?: string | null
  plot?: PlotResponse | null
}
