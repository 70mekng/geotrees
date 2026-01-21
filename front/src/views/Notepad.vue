<template>
  <Toaster position="top-center" richColors/>
  <div class="notepad">
    <div class="card-info">

      <div class="info-img">
        <h3>Screenshot</h3>
        <div class="upload-img">
          <img v-if="currentNote.image_url" :src="currentNote.image_url" class="img-area" alt="note image">
          <div v-else tabindex="0" @focus="isUploadSelected = true" @blur="isUploadSelected = false" @paste="pasteImage"
            class="upload-area">
            <span v-if="!isUploadSelected">Click to enable upload by paste</span>
            <span v-else>Paste or select file</span>
            <input ref="fileInput" type="file" accept="image/png, image/jpeg, image/jpg, image/webp"
              @change="uploadImage" />
          </div>

        </div>
      </div>

      <div class="info-ocr">
        <h3>OCR</h3>
        {{ currentNote.ocr }}
      </div>


      <div class="info-memo">
        <h3>Memo</h3>
        <textarea 
          v-model="currentNote.memo"
          placeholder="Enter your memo"

          >
        </textarea>
      </div>

      <div class="info-analysis">
        <h3>AI Analysis</h3>
        {{ currentNote.analysis }}
      </div>
    </div>

    <div class="notepad-board">
      <div class="card-list">
        <NoteCard 
          @click="selectNote(note)" 
          :class="{ 'selected': currentNote.id === note.id }"
          v-for="note in notepad.notes" :key="note.id" :note="note">
        </NoteCard>
      </div>

      <div class="toolbar">
        <button @click="addNote">
          <img src="../assets/icons/new.svg" alt="new">
        </button>
        <button @click="updateNote" :disabled="!isDirty">
          <img src="../assets/icons/save.svg" alt="save">
        </button>
        <button @click="deleteNote">
          <img src="../assets/icons/delete.svg" alt="delete">
        </button>
        <button><img src="../assets/icons/analyze_all.svg" alt="analyze all">
        </button>
        <button @click="$router.push('/about')">
          <img src="../assets/icons/info.svg" alt="info">
        </button>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import NoteCard from '../components/NoteCard.vue'
import type { Note, Notepad } from '../types/types'
import * as api from '../server/api'

const notepad = ref<Notepad>({
  id: '',
  all_analysis: '',
  notes: [],
});
const currentNote = ref<Note>({
  id: '',
  notepad_id: '',
  image_url: '',
  ocr: '',
  memo: '',
  analysis: '',
  created_at: '',
});
const originalNote = ref<Note | null>(null);
const isUploadSelected = ref(false);
const isDirty = computed(() => {
  if (!currentNote.value) return false;

  if (!originalNote.value?.id) {
    return !!(currentNote.value.image_url || currentNote.value.ocr || currentNote.value.memo);
  }

  return (
    currentNote.value.image_url !== originalNote.value.image_url ||
    currentNote.value.ocr !== originalNote.value.ocr ||
    currentNote.value.memo !== originalNote.value.memo
  );
});


const route = useRoute();
const router = useRouter();
let notepadId = route.params.notepadId as string | null;
if (!notepadId) {
  notepadId = '';
}

const toast = useToast();

async function loadNotepad() {
  if (notepadId) {
    notepad.value = await api.getNotepad(notepadId);
  } else {
    try {
      const result = await api.createNotepad()
      notepad.value = result
      notepadId = result.id;
      console.log('result', result);
      router.replace({ name: 'notepad', params: { notepadId: result.id } })
    } catch (err) {
      console.error('error:', err)
    }
  }
}

async function analyzeNotepad(id: string) {
  // TODO
}

function selectNote(note: Note) {
  currentNote.value = note;
  originalNote.value = {...note};
}

async function addNote() {
  currentNote.value = {
    id: '',
    notepad_id: '',
    image_url: '',
    ocr: '',
    memo: '',
    analysis: '',
    created_at: '',
  }
  originalNote.value = null;
}

async function updateNote() {
  if (!notepadId) {
    console.error(notepadId, 'notepadId is null');
    toast.error('Notepad not found');
    return;
  }

  // new note
  if (!currentNote.value?.id) {
    const newNote = await api.createNote(notepadId, {
      image_url: currentNote.value.image_url,
      ocr: currentNote.value.ocr,
      memo: currentNote.value.memo,
    });
    currentNote.value = newNote;
    console.log('newNote', newNote);
    notepad.value?.notes.push(newNote);
  }
  // update note
  else {
    await api.updateNote(currentNote.value.id, currentNote.value);
  }

  originalNote.value = {...currentNote.value};
}

async function deleteNote() {
  if (!currentNote.value || !notepadId) return;
  if (currentNote.value.id === '') {
    addNote();
    return;
  }

  const result = await api.deleteNote(currentNote.value.id);
  toast.success(result.message);

  if (notepad.value?.notes) {
    notepad.value.notes = notepad.value.notes.filter(
      n => n.id !== currentNote.value!.id
    );
  }

  currentNote.value = {
    id: '',
    notepad_id: '',
    image_url: '',
    ocr: '',
    memo: '',
    analysis: '',
    created_at: '',
  };
}

async function pasteImage(e: ClipboardEvent) {
  const items = e.clipboardData?.items;
  if (!items) return

  for (const item of items) {
    if (item.type.startsWith('image/')) {
      const file = item.getAsFile()
      if (!file) return

      const imageUrl = await api.uploadImage(file)
      if (!currentNote.value) return
      currentNote.value.image_url = imageUrl
      break
    }
  }
}

async function uploadImage(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (!file) return;

  const imageUrl = await api.uploadImage(file)
  if (!currentNote.value) {
    console.error('currentNote is null');
    return;
  }
  currentNote.value.image_url = imageUrl;
}

async function processOCR(imageUrl: string) {
  // TODO
}

async function analyzeNote(data: object) {
  // TODO
}

onMounted(() => {
  loadNotepad();
});
</script>

<style scoped lang="scss">
.notepad {
  display: flex;
  height: 100%;
  width: 100%;

  font-size: 20px;

  overflow-y: hidden;

  .card-info {
    background-color: #ebd7c7;

    display: flex;
    flex-direction: column;
    gap: 15px;

    box-shadow:
      0px 0 4px 4px #551601c8,
      0px 0 8px 4px #5516016e,
      rgba(80, 62, 8, 0.25) 0px 0px 10px -20px,
      rgba(0, 0, 0, 0.3) 0px 30px 20px -30px,
      rgba(64, 43, 10, 0.35) 0px 0px 6px 0px inset;


    height: 100%;
    width: 500px;
    padding: 20px 40px;

    overflow-y: auto;

    h3 {
      // font-family: 'Baloo Bhaijaan 2', cursive;
      // margin: 0;
      margin-bottom: 5px;
      font-family: 'Lexend Deca', sans-serif;
      font-size: 24px;
      font-weight: 600;
      // font-style: italic;
      color: #333;
    }

    .info-img {
      width: 100%;
      flex-shrink: 0;

      .upload-img {
        background-color: #F4EBD3;
        width: 100%;
        height: 220px;

        .upload-area {
          display: flex;
          flex-direction: column;
          gap: 20px;
          align-items: center;
          justify-content: center;

          width: 100%;
          height: 100%;

          border: 3px solid #875325;
          cursor: pointer;

          &:focus {
            border: 3px dashed #875325;
            box-shadow: 0 0 10px 0 rgba(135, 83, 37, 0.5);
          }

          input {
            background-color: #e5b89c;
          }
        }

        .img-area {
          width: 100%;
          height: 100%;
          object-fit: contain;

          border: 3px solid #875325;
          // box-shadow: 0 0 10px 0 rgba(135, 83, 37, 0.5);
        }
      }
    }

    .info-memo {
      width: 100%;

      textarea {
        background-color: #F4EBD3;
        
        width: 100%;
        min-height: 100px;
        padding: 10px;

        border: 3px solid #875325;

        font-size: 20px;
        font-family: 'Lexend Deca', sans-serif;
        resize: vertical;

        &focus {
          outline: none;
          border: 3px solid #875325;
          // box-shadow: 0 0 10px 0 rgba(135, 83, 37, 0.5);
        }
    }
    }
  }

  .notepad-board {
    // background-color: #d5d5d5;
    flex: 1;
    display: flex;
    flex-direction: column;


    position: relative;
    height: 100%;
    min-height: 500px;
    overflow-y: auto;

    .card-list {
      flex: 1;
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 30px;
      align-content: start;

      padding: 20px 20px 70px 40px;
      
    }


    .toolbar {
      background: rgba(255, 255, 255, 0.15);

      display: flex;
      flex-direction: row;
      gap: 40px;
      align-items: center;
      justify-content: center;

      position: sticky;
      left: 0;
      right: 0;
      bottom: 40px;
      width: fit-content;
      margin: 0 auto;
      padding: 10px 40px;
      
      border: 1px solid rgba(255, 255, 255, 0.8);
      border-radius: 2rem;
      backdrop-filter: blur(2px) saturate(180%);
      box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2), inset 0 4px 20px rgba(255, 255, 255, 0.3);



      button {
        background-color: #f2bd87;

        display: flex;
        align-items: center;
        justify-content: center;
        width: 70px;
        height: 70px;

        border-radius: 50%;
        border: 4px solid rgb(0, 0, 0);
        border-radius: 2rem;
        backdrop-filter: blur(2px) saturate(180%);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2), inset 0 4px 20px rgba(255, 255, 255, 0.3);
        
        cursor: pointer;

        &:hover {
          animation: rippleShadow 1.5s linear infinite;
        }

        &:disabled {
          background-color: #979393;
          cursor: not-allowed;
          animation: none;
        }

        img {
          color: #d77777;
          width: 70%;
          height: 70%;
        }
      }
    }
  }
}

@keyframes rippleShadow {
  0% {
    box-shadow:
      0 0 0 0 rgba(178, 110, 92, 0.6),
      0 0 0 0 rgba(178, 110, 92, 0.4);
  }

  40% {
    box-shadow:
      0 0 0 15px rgba(178, 110, 92, 0.3),
      0 0 0 5px rgba(178, 110, 92, 0.5);
  }

  100% {
    box-shadow:
      0 0 0 25px rgba(178, 110, 92, 0),
      0 0 0 20px rgba(178, 110, 92, 0);
  }

}
</style>