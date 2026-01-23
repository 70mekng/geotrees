<template>
  <div class="about">
    <h1>About</h1>

    <div class="about-section">
      <div class="about-section-title">
        The GeoTrees are Lost
      </div>
      <div class="about-section-content">
        <p>
          GeoTrees Lost is an AI-powered assistant for geography guessing games. It helps you analyze screenshots and organize clues in untimed game modes — things like road signs, vegetation, architecture, and language hints.
          <br>
          To be honest, AI can't pinpoint exact locations or streets. That level of precision belongs to the true masters who've memorized road markings across continents. This tool just helps you gather and sort your observations.
        </p>
        <p>
          The name comes from The Roottrees are Dead, a game about investigating documents and records to complete a family tree.
          I like these analytical games, especially the ones without horror elements. Watching skilled players pinpoint locations in GeoGuessr is surprisingly fun.
        </p>
      </div>
    </div>

    <div class="about-section">
      <div class="about-section-title">
        Tech Stack
      </div>
      <div class="about-section-content">
        <p>
          Vue + TypeScript on the frontend, Python + FastAPI + SQLAlchemy on the backend. Images on AWS S3, OCR by Google Cloud Vision, AI by OpenAI. Still on SQLite as I type this — AWS deployment is next on the list.
        </p> 
        <p>
          Picked up a few of these along the way while building this. I know I still have a lot to learn, but I'm a fast learner and genuinely excited about the opportunity to grow with your team.
          (Mobile layout not yet optimized due to time constraints.)
        </p>
      </div>
    </div>

    <div class="about-section">
      <div class="about-section-title">
        How to use
      </div>
      <div class="about-section-content">
        <p>
          Upload or paste your screenshot. 
          Hit OCR to extract text — useful for identifying languages and narrowing down the country. 
          Add your own notes below, or just use it as a notepad without screenshots. 
        </p>
        <p>
          <!-- <br> -->
          Once you save a note, you can click AI Analyze to let GPT-4o take a look. 
          You can also hit Analyze All for a comprehensive analysis across all your notes.
        </p>
      </div>
    </div>

    <div class="about-section">
      <div class="about-section-title">
        Start a new notepad
      </div>
      <div class="about-section-content">
        <p>Click <router-link to="/notepad">here</router-link> to start a new session.</p>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.about {
  display: flex;
  flex-direction: column;
  gap: 20px;

  height: 100vh;
  width: 100vw;
  padding: 40px 80px; 

  font-size: 20px;
  overflow-y: auto;

  .about-section {
    /* background-color: #F6E6DB; */
    background-color: #CBB5A3;
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 15px 4px 4px 4px;

    .about-section-title {
      padding: 0 20px;
      font-size: 24px;
      font-weight: 600;
    }

    .about-section-content {
      background-color: #F6E6DB;

      display: flex;
      flex-direction: column;
      gap: 20px;
      padding: 20px 30px;
      font-size: 20px;
    }
  }
}
</style>