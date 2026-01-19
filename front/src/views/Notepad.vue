<template>
  <div class="notepad">
    <div class="card-info">
      <div class="info-img">
        img
      </div>
      <div class="info-ocr">
        ocr
      </div>
      <div class="info-memo">
        memo
      </div>
      <div class="info-analysis">
        analysis
      </div>
    </div>
    
    <div class="notepad-board">
      <div class="card-list">
      </div>

      <div class="toolbar">
        <button>new</button>
        <button>save</button>
        <button>delete</button>
        <button>analyze all</button>
        <button>about</button>
      </div>
    </div>

    <div class="notepad-analysis">
      all analysis
    </div>

  </div>
</template>

<script setup lang="ts">
  import { ref, computed } from 'vue'
  import type { Note, Notepad } from '../types/types'
  import * as api from '../server/api'

  const notepad = ref<Notepad | null>(null)
  const currentNote = ref<Note | null>(null)
  const notes = computed(() => notepad.value?.notes ?? [])

  async function getNotepad(id: string) {
    // TODO
  }
  
  async function analyzeNotepad(id: string) {
    // TODO
  }

  async function addNote() {
    // TODO
  }

  async function updateNote(note: Note) {
    // TODO
  }

  async function deleteNote() {
    // TODO
  }

  async function uploadImage(file: File) {
    // TODO
  }

  async function processOCR(imageUrl: string) {
    // TODO
  }

  async function analyzeNote(data: object) {
    // TODO
  }
  

</script>

<style scoped lang="scss">

</style>