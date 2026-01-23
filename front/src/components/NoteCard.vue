<template>
  <div class="note-card">
    <div v-if="note.image_url" class="note-card-img">
      <img :src="note.image_url" alt="note image">
    </div>
    <!-- <div v-if="note.ocr" class="note-card-ocr">
      {{ note.ocr.length > 100 ? note.ocr.substring(0, 50) + '...' : note.ocr }}
    </div>
    <div v-if="note.memo" class="note-card-memo">
      {{ (note.memo.length > 80 && note.image_url) ? note.memo.substring(0, 80) + '...' : note.memo }}
    </div>
    <div v-if="note.analysis" class="note-card-analysis">
      {{ note.analysis.length > 120 ? note.analysis.substring(0, 120) + '...' : note.analysis }}
    </div> -->
    <div v-if="!note.image_url && note.memo" class="note-card-memo">
      {{ (note.memo.length > 80 && note.image_url) ? note.memo.substring(0, 80) + '...' : note.memo }}
    </div>

  </div>
</template>

<script setup lang="ts">
  import type { Note } from '../types/types';
  const props = defineProps<{note: Note}>();
</script>

<style scoped lang="scss">
  .note-card {
    width: 100%;
    background-color: #fff;

    display: flex;
    flex-direction: column;
    gap: 10px;

    min-width: 0;
    // height: 500px;
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

    .note-card-img, .note-card-ocr, .note-card-memo, .note-card-analysis {
      height: 150px;
      width: 100%;
      white-space: pre-line;
      word-break: break-all;

      overflow: hidden;
    }

    .note-card-img {
      background-color: #e7e7e7;
      // height: 150px;

      
      img {
          width: 100%;
          height: 100%;
          object-fit: contain;
      }
    }

    .note-card-ocr {
      background-color: #F7DED3;
      font-size: 18px;
      color: #333;
      padding: 10px;

      max-height: 100px;
    }
    
    .note-card-memo {
      background-color: #EDD1B0;
      font-size: 18px;
      color: #333;
      padding: 10px;
    }
    
    .note-card-analysis {
      flex: 1;
      background-color: #e5d2bd;
      font-size: 18px;
      color: #333;
      padding: 10px;
      border-radius: 0 0 15px 15px;
      min-width: 0;
    }


  }
</style>