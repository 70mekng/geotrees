import type { Notepad } from '@/types/types';
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.response.use(
  res => res,
  err => {
    console.error('API Error:', err.response?.data || err.message);
    throw err;
  }
);

// Note
export async function createNote(notepadId: string, data: {
  image_url: string
  ocr: string
  memo: string
}) {
  const response = await api.post(`/notepad/${notepadId}/note`, {
    image_url: data.image_url,
    ocr: data.ocr,
    memo: data.memo,
  });
  return response.data;
}

export async function updateNote(noteId: string, data: object) {
  const response = await api.patch(`/note/${noteId}`, data);
  return response.data;
}

export async function deleteNote(noteId: string) {
  const response = await api.delete(`/note/${noteId}`);
  return response.data;
}

// Notepad
export async function createNotepad() {
  const response = await api.post('/notepad');
  return response.data;
}

export async function getNotepad(notepadId: string) {
  const response = await api.get(`/notepad/${notepadId}`);
  return response.data;
}

// functions
export async function uploadImage(file: File) {
  const extension = file.name.split('.').pop()
  if (!extension) {
    throw new Error('Invalid file type')
  }

  const res = await api.post(`/upload?extension=${extension}`)
  const { upload_url, image_url } = res.data;

  await fetch(upload_url, {
    method: 'PUT',
    body: file,
    headers: {
      'Content-Type': `image/${extension}`
    }
  })

  return image_url
}

export async function ocr(imageUrl: string) {
  const response = await api.post('/ocr', { image_url: imageUrl });
  return response.data;
}

export async function analyze(noteId: string) {
  const response = await api.post(`/note/${noteId}/analyze`);
  return response.data;
}

export async function analyzeAll(notepadId: string) {
  const response = await api.post(`/notepad/${notepadId}/analyze`);
  return response.data;
}