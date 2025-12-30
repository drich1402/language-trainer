<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="12">
        <v-card class="elevation-12">
          <v-card-title class="text-h5 text-center pa-6 bg-primary">
            <span class="text-white">German-Spanish Vocabulary Trainer</span>
          </v-card-title>

          <v-card-text class="pa-6">
            <h2 class="text-h5 mb-4">Register</h2>

            <v-form ref="form" v-model="valid" @submit.prevent="handleRegister">
              <v-text-field
                v-model="email"
                label="Email"
                type="email"
                :rules="[rules.required, rules.email]"
                prepend-inner-icon="mdi-email"
                variant="outlined"
                class="mb-2"
              />

              <v-text-field
                v-model="password"
                label="Password"
                :type="showPassword ? 'text' : 'password'"
                :rules="[rules.required, rules.minLength]"
                prepend-inner-icon="mdi-lock"
                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="showPassword = !showPassword"
                variant="outlined"
                class="mb-2"
              />

              <v-text-field
                v-model="confirmPassword"
                label="Confirm Password"
                :type="showConfirmPassword ? 'text' : 'password'"
                :rules="[rules.required, rules.passwordMatch]"
                prepend-inner-icon="mdi-lock-check"
                :append-inner-icon="
                  showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'
                "
                @click:append-inner="showConfirmPassword = !showConfirmPassword"
                variant="outlined"
                class="mb-4"
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
                Register
              </v-btn>

              <v-divider class="my-4" />

              <p class="text-center">
                Already have an account?
                <router-link to="/login" class="text-primary">
                  Login here
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
const confirmPassword = ref("");
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const rules = {
  required: (value) => !!value || "Required.",
  email: (value) => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return pattern.test(value) || "Invalid email.";
  },
  minLength: (value) => value.length >= 6 || "Minimum 6 characters.",
  passwordMatch: (value) => value === password.value || "Passwords must match.",
};

const handleRegister = async () => {
  if (!valid.value) return;

  loading.value = true;
  error.value = "";

  const result = await authStore.register(email.value, password.value);

  loading.value = false;

  if (result.success) {
    router.push("/quiz");
  } else {
    error.value = result.error;
  }
};
</script>
