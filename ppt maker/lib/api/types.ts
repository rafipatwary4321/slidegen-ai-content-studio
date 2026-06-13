export type Persona = "Student" | "Business" | "Marketing" | "Corporate";
export type Theme = "Cinematic Dark" | "Professional Light";

export interface UploadedFileMeta {
  filename: string;
  content_type: string;
  extension: string;
  size_bytes: number;
  file_hash: string;
  parser_status: string;
  word_count: number;
  character_count: number;
  preview_snippet: string;
}

export interface ParsedDocument {
  metadata: UploadedFileMeta;
  extracted_text: string;
  prepared_text: string;
}

export interface SlideOutlineItem {
  slide_number: number;
  title: string;
  bullets: string[];
}

export interface SpeakerNoteItem {
  slide_number: number;
  note: string;
}

export interface DocumentAnalysis {
  filename: string;
  document_type: string;
  persona: Persona | string;
  /** When set by the model, a suggested deck theme matching backend literals. */
  recommended_theme?: Theme | null;
  presentation_title: string;
  summary: string;
  word_count: number;
  key_topics: string[];
  chart_suggestions: string[];
  outline: SlideOutlineItem[];
  speaker_notes: SpeakerNoteItem[];
  sentiment: string;
}

export interface UploadResponse {
  success: boolean;
  message: string;
  upload: ParsedDocument;
}

export interface AnalyzeResponse {
  success: boolean;
  message: string;
  parsed_document: ParsedDocument;
  analysis: DocumentAnalysis;
}

export interface GenerateOutlineRequest {
  document_summary: string;
  persona: Persona;
  theme: Theme;
  prompt?: string;
  max_slides: number;
}

export interface GenerateOutlineResponse {
  success: boolean;
  message: string;
  outline: SlideOutlineItem[];
}

export interface ReviseOutlineRequest {
  instruction: string;
  persona: Persona;
  theme: Theme;
  outline: SlideOutlineItem[];
  presentation_id?: string;
  user_id?: string;
}

export interface ReviseOutlineResponse {
  success: boolean;
  message: string;
  previous_outline: SlideOutlineItem[];
  updated_outline: SlideOutlineItem[];
}

export interface ExportPptxRequest {
  title: string;
  theme: Theme;
  slides: SlideOutlineItem[];
  speaker_notes: SpeakerNoteItem[];
  presentation_id?: string;
  user_id?: string;
}

export interface ExportResult {
  export_id: string;
  title: string;
  theme: string;
  slide_count: number;
  file_path: string;
  download_url: string;
  status: string;
}

export interface ExportPptxResponse {
  success: boolean;
  message: string;
  export: ExportResult;
}

export interface PresentationRecord {
  id: string;
  title: string;
  uploaded_filename: string;
  user_id?: string | null;
  persona: string;
  theme: string;
  created_at: string;
  outline: SlideOutlineItem[];
  speaker_notes: SpeakerNoteItem[];
  pptx_file_path: string | null;
}

export interface SavePresentationRequest {
  title: string;
  uploaded_filename: string;
  persona: Persona;
  theme: Theme;
  outline: SlideOutlineItem[];
  speaker_notes: SpeakerNoteItem[];
  pptx_file_path?: string | null;
  user_id?: string;
}

export interface SavePresentationResponse {
  success: boolean;
  message: string;
  presentation: PresentationRecord;
}

export interface ListPresentationsResponse {
  success: boolean;
  presentations: PresentationRecord[];
}

export interface AuthUser {
  id: string;
  email: string;
  name?: string | null;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  user: AuthUser;
}
