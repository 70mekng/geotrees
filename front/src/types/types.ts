export interface Notepad {
    id: string
    all_analysis: string | null
    notes: Note[]
}

export interface Note {
    id: string
    notepad_id: string
    image_url: string | null
    ocr: string | null
    memo: string | null
    analysis: string | null
    created_at: string
}

