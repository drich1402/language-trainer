<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="12">
        <v-card class="elevation-12">
          <v-card-title class="text-h5 text-center pa-6 bg-primary">
            <span class="text-white">German-Spanish Vocabulary Trainer</span>
          </v-card-title>

          <v-card-text class="pa-6">
            <h2 class="text-h5 mb-4">Login</h2>

            <v-form ref="form" v-model="valid" @submit.prevent="handleLogin">
              <v-text-field
                v-model="email"
                label="Email"
                type="email"
                :rules="[rules.required, rules.email]"
                prepend-inner-icon="mdi-email"
                variant="outlined"
                class="mb-2"
                autocomplete="email"
                persistent-placeholder
              />

              <v-text-field
                v-model="password"
                label="Password"
                :type="showPassword ? 'text' : 'password'"
                :rules="[rules.required]"
                prepend-inner-icon="mdi-lock"
                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="showPassword = !showPassword"
                variant="outlined"
                class="mb-4"
                autocomplete="current-password"
                persistent-placeholder
              />

              <v-alert v-if="error" type="error" class="mb-4">
                {{ error }}
              </v-alert>

              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                :loading="loading"
                :disabled="!valid"
              >
                Login
              </v-btn>

              <v-divider class="my-4" />

              <p class="text-center">
                Don't have an account?
                <router-link to="/register" class="text-primary">
                  Register here
                </router-link>
              </p>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth";
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const authStore = useAuthStore();

const form = ref(null);
const valid = ref(false);
const loading = ref(false);
const error = ref("");

const email = ref("");
const password = ref("");
const showPassword = ref(false);

const rules = {
  required: (value) => !!value || "Required.",
  email: (value) => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return pattern.test(value) || "Invalid email.";
  },
};

const handleLogin = async () => {
  if (!valid.value) return;

  loading.value = true;
  error.value = "";

  const result = await authStore.login(email.value, password.value);

  loading.value = false;

  if (result.success) {
    router.push("/quiz");
  } else {
    error.value = result.error;
  }
};
</script>
