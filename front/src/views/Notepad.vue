<template>
  <Toaster position="top-center" richColors/>
  <div class="notepad">
    <div class="card-info">

      <div class="info-img">
        <div class="info-section-title">
          <h3>Screenshot</h3>
        </div>
        <div class="upload-img">
          <img 
            v-if="currentNote.image_url" 
            :src="currentNote.image_url" 
            class="img-area" 
            alt="note image"
            @click="isImgZoom = true"
          >
          <div 
            v-else 
            tabindex="0" 
            @focus="isUploadSelected = true" 
            @blur="isUploadSelected = false" 
            @paste="pasteImage"
            class="upload-area">
              <span v-if="!isUploadSelected">Click to enable upload by paste</span>
              <span v-else>Paste or select file</span>
              <input 
                ref="fileInput"  
                type="file" 
                accept="image/png, image/jpeg, image/jpg, image/webp"
                @change="uploadImage" />
          </div>

        </div>
      </div>

      <div class="info-ocr">
        <div class="info-section-title">
          <h3>OCR</h3>
          <button 
            @click="ocrImage"
            :disabled="!currentNote.image_url">
            <img class="button-icon" src="../assets/icons/ocr.svg" alt="ocr">
            <span class="button-text">Click to OCR</span>
          </button>
        </div>
        <textarea 
          v-if="currentNote.ocr"
          v-model="currentNote.ocr"
          placeholder="Click on analyze button to get OCR. And you can edit the OCR text.">
        </textarea>
      </div>


      <div class="info-memo">
        <div class="info-section-title">
          <h3>Memo</h3>
        </div>
        <textarea 
          v-model="currentNote.memo"
          placeholder="Enter your memo">
        </textarea>
      </div>

      <div class="info-analysis">
        <div class="info-section-title">
          <h3>AI Analysis</h3>
          <button 
            @click="analyzeNote"
            :disabled="!currentNote.ocr && !currentNote.image_url && !currentNote.memo">
            <img class="button-icon" src="../assets/icons/analyze.svg" alt="analyze">
            <span class="button-text">Click to analyze</span>
          </button>
        </div>
        <textarea 
          v-model="currentNote.analysis"
          v-if="currentNote.analysis"
          placeholder="Click on analyze button to get analysis">
        </textarea>
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
        <button 
          @click="notepad.all_analysis ? isAnalyzeAllDisplayed = true : analyzeNotepad()">
          <img src="../assets/icons/analyze_all.svg" alt="analyze all">
        </button>
        <button @click="$router.push('/about')">
          <img src="../assets/icons/info.svg" alt="info">
        </button>
      </div>
    </div>

    <div 
      v-if="isImgZoom"
      class="img-zoom"
      @click="isImgZoom = false">
      <img :src="currentNote.image_url" alt="note image">
    </div>

    <div 
      v-if="isAnalyzeAllDisplayed"
      class="all-result">
      <div 
        @click="isAnalyzeAllDisplayed = false"
        class="overlay">
      </div>
      <div 
        class="all-result-Dialog">
        <div class="all-result-header">
          <h3>Notepad analyzed result</h3>
          <button @click="analyzeNotepad">Re-analyze</button>
        </div>
        <div class="all-result-content">
          <div v-if="isAnalyzeAllLoading">
            <span>Analyzing...</span>
          </div>
          <div v-else>
            {{ notepad.all_analysis }}
          </div>
        </div>
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
const isImgZoom = ref(false);
const isAnalyzeAllLoading = ref(false);
const isAnalyzeAllDisplayed = ref(false);
const isDirty = computed(() => {
  if (!currentNote.value) return false;

  if (!originalNote.value?.id) {
    return !!(currentNote.value.image_url || currentNote.value.ocr || currentNote.value.memo || currentNote.value.analysis );
  }

  return (
    currentNote.value.image_url !== originalNote.value.image_url ||
    currentNote.value.ocr !== originalNote.value.ocr ||
    currentNote.value.memo !== originalNote.value.memo ||
    currentNote.value.analysis !== originalNote.value.analysis
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

async function ocrImage() {
  if (!currentNote.value?.image_url) {
    console.error('image_url is null');
    toast.error('Image is not uploaded');
    return;
  }
  const data = await api.ocr(currentNote.value.image_url);
  console.log('ocr data', data);
  currentNote.value.ocr = data.ocr;
}

async function analyzeNote() {
  if (!currentNote.value.id) {
    console.error('note id is null');
    toast.error('The note id is blank. Please save the note first.');
    return;
  } 
  if (!isDirty) {
    toast.error('The note is changed. Please save the note first.');
    return;
  }

  try {
    currentNote.value.analysis = 'Analyzing...';
    const response = await api.analyze(currentNote.value.id);
    currentNote.value.analysis = response.analysis;
  } catch (err) {
    console.error('error:', err);
    toast.error('Failed to analyze note');
  }
  const response = await api.analyze(currentNote.value.id);
  if (!response.analysis) {
    console.error('analysis is null');
    toast.error('Failed to analyze note');
    return;
  }
  currentNote.value.analysis = response.analysis;
}

async function analyzeNotepad() {
  if (!notepadId) {
    console.error('notepadId is null');
    toast.error('Notepad id is blank. Please reload the page.');
    return;
  }
  if (!isDirty) {
    toast.error('Some notes may be changed. Please save the notes first.');
    return;
  }

  isAnalyzeAllDisplayed.value = true;
  isAnalyzeAllLoading.value = true;
  try {
    const result = await api.analyzeAll(notepadId);
    console.log('result', result);
    notepad.value.all_analysis = result.analysis;
  } catch (err) {
    console.error('error:', err);
    toast.error('Failed to analyze notepad');
  } finally {
    isAnalyzeAllLoading.value = false;
  }
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

    height: 100%;
    width: 30%;
    min-width: 500px;
    padding: 20px 30px;
    overflow-y: auto;

    box-shadow:
      0px 0 4px 4px #551601c8,
      0px 0 8px 4px #5516016e,
      rgba(80, 62, 8, 0.25) 0px 0px 10px -20px,
      rgba(0, 0, 0, 0.3) 0px 30px 20px -30px,
      rgba(64, 43, 10, 0.35) 0px 0px 6px 0px inset;

    .info-img {
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

    .info-ocr {
      textarea {
        min-height: 100px;
      }
    }

    .info-memo {

      textarea {
        min-height: 100px;
      }
    }

    .info-analysis {
      textarea {
        min-height: 200px;
      }
    }

    .info-img, .info-ocr, .info-memo, .info-analysis {
      width: 100%;

      .info-section-title {
        // background-color: #773c00;
        display: flex;
        flex-direction: row;
        gap: 10px;
        align-items: center;
        justify-content: space-between;

        padding: 10px 0;

        h3 {
          color: #333;
          
          font-family: 'Lexend Deca', sans-serif;
          font-size: 24px;
          font-weight: 600;
        }

        button {
          display: flex;
          align-items: center;
          position: relative;
          height: 40px;
          width: 240px;

          outline: 3px solid #976e56;
          border: none;
          cursor: pointer;
          
          .button-icon, .button-text {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            transition: all 0.3s;
            overflow: hidden;
            flex-shrink: 0;
          }

          .button-icon {
            background-color: #e9e4df;
            width: 40px;
            padding: 4px;
          }

          .button-text {
            background-color: #976e56;
            color: #e9e4df;
            width: 200px;
            padding: 0 10px;
            font-size: 22px;
            font-weight: 600;
          }

          &:hover .button-icon {
            width: 240px;
          }

          &:hover .button-text {
            width: 0;
            padding: 0;
            opacity: 0;
          }

          &:not(:hover) .button-icon,
          &:not(:hover) .button-text {
            transition: all 0.6s ease-in-out;
          }
        }

      }
    }

    .info-ocr, .info-memo, .info-analysis {
      background-color: #bea996ba;
      padding: 0 10px 5px 10px;

      textarea {
        background-color: #f6e6db;
        
        width: 100%;
        padding: 10px;
        border: none;

        font-size: 20px;
        font-family: 'Lexend Deca', sans-serif;
        resize: vertical;

        &:focus {
          background-color: #eac9a1;
          outline: 2px solid #875325;
        }
      }
    }
  }

  .notepad-board {
    background: url('../assets/bg.svg') no-repeat center center;
    background-size: cover;
    
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
      
      // border: 1px solid rgba(255, 255, 255, 0.8);
      // border-radius: 2rem;
      // backdrop-filter: blur(2px) saturate(180%);
      // box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2), inset 0 4px 20px rgba(255, 255, 255, 0.3);



      button {
        background-color: rgba(242, 171, 135, 0.15);
        // background: rgba(255, 255, 255, 0.15);

        display: flex;
        align-items: center;
        justify-content: center;
        width: 70px;
        height: 70px;

        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 2rem;
        backdrop-filter: blur(2px) saturate(180%);
        box-shadow: 
          0 8px 32px rgba(31, 38, 135, 0.2), 
          0 4px 4px rgba(135, 78, 31, 0.5), 
          inset 0 4px 20px rgba(255, 255, 255, 0.3);

        // border-radius: 50%;
        // border: 4px solid rgb(0, 0, 0);
        // border-radius: 2rem;
        // backdrop-filter: blur(2px) saturate(180%);
        // box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2), inset 0 4px 20px rgba(255, 255, 255, 0.3);
        
        cursor: pointer;

        &:hover {
          animation: rippleShadow 1.5s linear infinite;
        }

        &:disabled {
          background-color: rgb(151, 147, 148, 0.65);
          cursor: not-allowed;
          animation: none;
        }

        img {
          color: #d77777;
          width: 70%;
          height: 70%;

          filter: drop-shadow(0 0 4px rgba(255, 255, 255, 0.805));
        }
      }
    }
  }

  .img-zoom {
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    position: absolute;
    height: 100%;
    width: 100%;
    margin: 0 auto;
    padding: 10px 0;
  }

  .all-result {
    // background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;

    position: absolute;
    height: 100%;
    width: 100%;
    margin: 0 auto;
    padding: 10px 0;

    .overlay {
      position: absolute;
      height: 100%;
      width: 100%;
      background-color: rgba(0, 0, 0, 0.5);
    }

    .all-result-Dialog {
      background-color: #f6e6db;

      display: flex;
      flex-direction: column;
      gap: 20px;
      height: 80%;
      width: 80%;
      padding: 40px;
      border-radius: 10px;
      box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.5);
      
      font-size: 24px;
      font-family: 'Lexend Deca', sans-serif;

      overflow-y: auto;
      z-index: 1000;

      .all-result-header {
        display: flex;
        flex-direction: row;
        gap: 10px;
        align-items: center;
        justify-content: space-between;

        button {
          background-color: #d4946e;
          color: #fff9f6;
          height: 100%;
          width: 200px;
          padding: 0 10px;
          font-size: 22px;
          font-weight: 600;
          
          border: none;
          cursor: pointer;

          transition: all 0.3s;
          
          &:hover {
            background-color: #d34d2e;
          }
        }
      }

      .all-result-content {
        white-space: pre-line;
        word-break: break-all;
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