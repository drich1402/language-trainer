<template>
  <v-container class="py-8">
    <v-row>
      <v-col cols="12">
        <v-card class="mb-6">
          <v-card-title class="d-flex justify-space-between align-center">
            <span class="text-h5">Vocabulary Quiz</span>
            <v-btn icon @click="logout">
              <v-icon>mdi-logout</v-icon>
            </v-btn>
          </v-card-title>
        </v-card>

        <!-- Statistics -->
        <v-row class="mb-6">
          <v-col cols="12" sm="6" md="3">
            <v-card color="primary">
              <v-card-text class="text-center text-white">
                <div class="text-h4">{{ stats.total_reviews }}</div>
                <div>Total Reviews</div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-card color="success">
              <v-card-text class="text-center text-white">
                <div class="text-h4">{{ stats.accuracy }}%</div>
                <div>Accuracy</div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-card color="info">
              <v-card-text class="text-center text-white">
                <div class="text-h4">{{ stats.words_learned }}</div>
                <div>Words Learned</div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-card color="warning">
              <v-card-text class="text-center text-white">
                <div class="text-h4">{{ stats.words_due }}</div>
                <div>Words Due</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Quiz Card -->
        <v-card v-if="currentQuestion" class="elevation-8">
          <v-card-text class="pa-8">
            <v-progress-linear
              v-if="showResult"
              :color="lastResult?.correct ? 'success' : 'error'"
              :model-value="100"
              height="6"
              class="mb-6"
            />

            <div class="text-center mb-8">
              <v-chip class="mb-4" color="primary" variant="outlined">
                {{ currentQuestion.word_class || "Word" }}
              </v-chip>
              <h1 class="text-h2 mb-2">{{ currentQuestion.german }}</h1>
              <p class="text-h6 text-medium-emphasis">
                What is the Spanish translation?
              </p>
            </div>

            <v-row>
              <v-col
                v-for="option in currentQuestion.options"
                :key="option.vocab_id"
                cols="12"
                md="6"
              >
                <v-btn
                  size="x-large"
                  block
                  :color="getButtonColor(option.vocab_id)"
                  :variant="getButtonVariant(option.vocab_id)"
                  :disabled="showResult"
                  @click="selectAnswer(option.vocab_id)"
                  class="text-h6 py-8"
                >
                  <v-icon start @click.stop="speakSpanish(option.spanish)"
                    >mdi-volume-high</v-icon
                  >
                  {{ option.spanish }}
                </v-btn>
              </v-col>
            </v-row>

            <v-alert
              v-if="showResult"
              :type="lastResult?.correct ? 'success' : 'error'"
              class="mt-6"
              variant="tonal"
            >
              <template v-if="lastResult?.correct">
                <strong>Correct!</strong>
              </template>
              <template v-else>
                <strong>Wrong!</strong> The correct answer is:
                <strong>{{ lastResult?.correct_answer }}</strong>
              </template>
            </v-alert>

            <div v-if="showResult" class="text-center mt-6">
              <v-btn
                size="large"
                color="primary"
                @click="nextQuestion"
                prepend-icon="mdi-arrow-right"
              >
                Next Question
              </v-btn>
            </div>
          </v-card-text>
        </v-card>

        <v-card v-else-if="loading" class="elevation-8">
          <v-card-text class="text-center pa-12">
            <v-progress-circular indeterminate color="primary" size="64" />
            <p class="mt-4">Loading question...</p>
          </v-card-text>
        </v-card>

        <v-card v-else class="elevation-8">
          <v-card-text class="text-center pa-12">
            <v-icon size="80" color="success">mdi-check-circle</v-icon>
            <h2 class="text-h4 mt-4 mb-2">🎉 All Done!</h2>
            <p class="text-h6 mb-4">
              You've reviewed all available vocabulary.
            </p>
            <p class="text-body-1 text-medium-emphasis mb-6">
              Come back later when more words are due for review, or practice
              the ones you've learned!
            </p>
            <div class="d-flex justify-center gap-2">
              <v-btn color="primary" size="large" @click="loadStats">
                Refresh Stats
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import api from "@/services/api";
import { useAuthStore } from "@/stores/auth";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const authStore = useAuthStore();

const loading = ref(false);
const currentQuestion = ref(null);
const selectedAnswer = ref(null);
const showResult = ref(false);
const lastResult = ref(null);
const startTime = ref(null);

const stats = ref({
  total_reviews: 0,
  correct_reviews: 0,
  wrong_reviews: 0,
  accuracy: 0,
  words_learned: 0,
  words_due: 0,
});

// Audio feedback
const successAudio = new Audio(
  new URL("@/assets/success.wav", import.meta.url).href
);
const failAudio = new Audio(new URL("@/assets/fail.wav", import.meta.url).href);

const playCorrectSound = () => {
  successAudio.currentTime = 0;
  successAudio.play();
};

const playIncorrectSound = () => {
  failAudio.currentTime = 0;
  failAudio.play();
};

const speakSpanish = (text) => {
  if ("speechSynthesis" in window) {
    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    // Replace "/" with a comma to create a natural pause
    const textToSpeak = text.replace(/\//g, ", ");

    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    utterance.lang = "es-ES"; // Spanish (Spain)
    utterance.rate = 0.9; // Slightly slower for clarity
    utterance.pitch = 1.0;

    window.speechSynthesis.speak(utterance);
  }
};

const loadStats = async () => {
  try {
    const newStats = await api.getStats();
    Object.assign(stats.value, newStats);
  } catch (error) {
    console.error("Failed to load stats:", error);
  }
};

const loadNextQuestion = async () => {
  loading.value = true;
  showResult.value = false;
  selectedAnswer.value = null;
  lastResult.value = null;

  try {
    currentQuestion.value = await api.getNextReview();
    startTime.value = Date.now();
    // Update stats after loading a new question to reflect words_due change
    await loadStats();
  } catch (error) {
    // 404 means no more vocabulary available - this is expected
    if (error.response?.status === 404) {
      currentQuestion.value = null;
    } else {
      console.error("Failed to load question:", error);
      currentQuestion.value = null;
    }
  } finally {
    loading.value = false;
  }
};

const selectAnswer = async (vocabId) => {
  const responseTime = Date.now() - startTime.value;

  try {
    lastResult.value = await api.submitReview(
      currentQuestion.value.vocab_id,
      vocabId,
      responseTime
    );
    selectedAnswer.value = vocabId;
    showResult.value = true;

    // Play sound based on result
    if (lastResult.value.correct) {
      playCorrectSound();
    } else {
      playIncorrectSound();
    }

    await loadStats();
  } catch (error) {
    console.error("Failed to submit answer:", error);
  }
};

const nextQuestion = () => {
  loadNextQuestion();
};

const getButtonColor = (vocabId) => {
  if (!showResult) return "primary";
  if (vocabId === lastResult.value?.correct_vocab_id) return "success";
  if (vocabId === selectedAnswer.value && !lastResult.value?.correct)
    return "error";
  return "grey";
};

const getButtonVariant = (vocabId) => {
  if (!showResult) return "elevated";
  if (vocabId === lastResult.value?.correct_vocab_id) return "flat";
  if (vocabId === selectedAnswer.value && !lastResult.value?.correct)
    return "flat";
  return "outlined";
};

const logout = () => {
  authStore.logout();
  router.push("/login");
};

onMounted(() => {
  loadStats();
  loadNextQuestion();
});
</script>
