<template>
  <div class="note-card">
    <div v-if="note.image_url" class="note-card-img">
      <img :src="note.image_url" alt="note image">
    </div>
    <div v-if="note.ocr" class="note-card-ocr">
      {{ note.ocr }}
    </div>
    <div v-if="note.memo" class="note-card-memo">
      {{ note.memo }}
    </div>
    <div v-if="note.analysis" class="note-card-analysis">
      {{ note.analysis }}
    </div>
  </div>
</template>

<script setup lang="ts">
  import type { Note } from '../types/types';
  const props = defineProps<{note: Note}>();
</script>

<style scoped lang="scss">
  .note-card {
    background-color: #fff;

    display: flex;
    flex-direction: column;
    gap: 10px;
    

    aspect-ratio: 3/4;
    padding: 20px;

    
    outline: 3px solid #875325;
    outline-offset: -3px;
    border-radius: 20px;
    box-shadow: 2px 2px 0 0 #915d2f9a;

    transition: all 0.5s cubic-bezier(0.65, 0, 0.076, 1);

    &.selected {
      background-color: #EBD7C7;
    }

    &:hover {
      transform: translate(-8px, -8px);
      box-shadow: 4px 4px 0 0 #875325;
      transition: all 0.3s cubic-bezier(0.65, 0, 0.076, 1);
    }

    .note-card-img {
        background-color: #e7e7e7;
        width: 100%;
        height: 150px;

        
        img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
    }

    .note-card-ocr, .note-card-memo, .note-card-analysis {
      width: 100%;
    }
  }
</style>