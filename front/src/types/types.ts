export interface Notepad {
    id: string
    all_analysis: string
    notes: Note[]
}

export interface Note {
    id: string
    notepad_id: string
    image_url: string
    ocr: string
    memo: string
    analysis: string
    created_at: string
}

