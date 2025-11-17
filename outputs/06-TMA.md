<reasoning>We need to produce detailed developer tasks, subtasks, expected files/modules, implementation notes. For each epic? The user wants detailed developer tasks. Likely for each sprint? They want a breakdown of tasks. We should produce a table or list of tasks for each epic, with subtasks, files/modules, notes. Provide in Markdown. Let's produce for each epic: E1, E2, E3, E4, E5, E6, E7, E8, E9. For each epic, list developer tasks, subtasks, expected files/modules, implementation notes. Provide clear structure. Use headings per epic. Provide tasks like "Implement authentication API", "Create user profile screen", etc. Provide subtask list. Provide expected files: e.g., src/api/auth.js, src/components/ProfileScreen.vue, etc. Implementation notes: e.g., use Firebase Auth, JWT, etc. Provide notes on architecture: use React Native, Swift, Kotlin, etc. Provide notes on AR: use ARKit/ARCore, etc. Provide notes on marketplace: use Stripe, etc. Provide notes on security: OWASP, encryption, etc. Provide notes on admin: use Node.js, Express, etc. Provide notes on performance: caching, lazy loading. Provide notes on tests: Jest, Detox, etc. Provide notes on CI/CD: GitHub Actions. Provide notes on documentation: Swagger, Storybook. Provide notes on code review: PR guidelines. Provide notes on versioning: semantic. Provide notes on environment variables. Provide notes on data models: User, WorkoutPlan, Exercise, ARPose, etc. Provide notes on database: PostgreSQL, Prisma. Provide notes on AR: use TensorFlow Lite for pose estimation. Provide notes on notifications: Firebase Cloud Messaging. Provide notes on analytics: Mixpanel. Provide notes on compliance: GDPR. Provide notes on performance: API response <2s, mobile memory <200MB. Provide notes on UI: design tokens, dark mode. Provide notes on accessibility: WCAG.

We need to output in clear Markdown. Let's produce a comprehensive table for each epic. Use headings like "## Epic E1 – Onboarding & Profile". Then "### Developer Tasks" list. Then "#### Subtasks" list. Then "#### Expected Files/Modules". Then "#### Implementation Notes". Provide for each epic. That will be long but okay. Let's produce.</reasoning># FitPulse – Detailed Developer Breakdown  
*(All dates and estimates are relative to the sprint plan above.  The team uses a mono‑repo with a shared **src/** folder for mobile code, a **backend/** folder for the API, and a **docs/** folder for Swagger/Storybook.)*

---

## Epic E1 – Onboarding & Profile

| # | Task | Sub‑tasks | Expected Files / Modules | Implementation Notes |
|---|------|-----------|--------------------------|----------------------|
| 1 | **Auth API** | • Design `/auth/register` & `/auth/login` endpoints.<br>• Implement JWT issuance & refresh.<br>• Add rate‑limit & brute‑force protection. | `backend/src/routes/auth.js`, `backend/src/controllers/authController.js`, `backend/src/middleware/auth.js` | Use **Passport.js** with **JWT strategy**. Store refresh tokens in a secure HTTP‑only cookie. |
| 2 | **Password Reset Flow** | • `/auth/forgot-password` (send email).<br>• `/auth/reset-password` (token validation). | `backend/src/routes/auth.js`, `backend/src/services/emailService.js` | Integrate **SendGrid**. Store reset tokens hashed in DB. |
| 3 | **Profile API** | • CRUD endpoints for user profile.<br>• Validation of age, gender, height, weight. | `backend/src/routes/user.js`, `backend/src/controllers/userController.js` | Use **Joi** for schema validation. |
| 4 | **Mobile Sign‑up Screen** | • Form fields (email, password, confirm).<br>• Client‑side validation.<br>• Call `/auth/register`. | `src/mobile/screens/SignUpScreen.{js,tsx}` | Use **React Native** + **Formik** + **Yup**. |
| 5 | **Mobile Login Screen** | • Email/password fields.<br>• Call `/auth/login`. | `src/mobile/screens/LoginScreen.{js,tsx}` | Store JWT in **SecureStore** (Expo) or Keychain (iOS). |
| 6 | **Profile Edit Screen** | • Editable fields (name, age, gender, height, weight).<br>• Submit to `/user`. | `src/mobile/screens/ProfileScreen.{js,tsx}` | Use **React Navigation** stack. |
| 7 | **Unit & Integration Tests** | • Jest tests for auth routes.<br>• Detox tests for mobile flows. | `backend/tests/auth.test.js`, `src/mobile/__tests__/SignUpScreen.test.js` | Aim for 90 % coverage. |
| 8 | **Documentation** | • Swagger docs for auth endpoints.<br>• Storybook stories for screens. | `docs/swagger.yaml`, `src/mobile/stories/ProfileScreen.stories.js` | Keep docs in sync with code via **swagger-jsdoc**. |

---

## Epic E2 – Personalised Workout Engine

| # | Task | Sub‑tasks | Expected Files / Modules | Implementation Notes |
|---|------|-----------|--------------------------|----------------------|
| 1 | **Workout Plan Model** | • Define `WorkoutPlan`, `WorkoutDay`, `Exercise` schemas.<br>• Store in PostgreSQL via **Prisma**. | `backend/prisma/schema.prisma` | Use `enum` for `difficulty`, `type`. |
| 2 | **AI Engine** | • Load pre‑trained model (TensorFlow Lite).<br>• Expose `/workouts/generate` endpoint. | `backend/src/services/workoutEngine.js` | Model takes user profile + goals → list of exercises. |
| 3 | **Caching Layer** | • Cache generated plans per user for 24 h.<br>• Use Redis. | `backend/src/services/cache.js` | Reduces compute cost. |
| 4 | **Mobile Workout List** | • Fetch `/workouts/generate` on first login.<br>• Render list of days & exercises. | `src/mobile/screens/WorkoutListScreen.{js,tsx}` | Use **FlatList** with lazy loading. |
| 5 | **Exercise Detail Screen** | • Show exercise name, description, video, and AR preview button. | `src/mobile/screens/ExerciseDetailScreen.{js,tsx}` | Video stored on **AWS S3**; stream via **react-native-video**. |
| 6 | **Unit Tests** | • Test engine logic with mock inputs.<br>• Test API response shape. | `backend/tests/workoutEngine.test.js` | Use **jest-mock** for model inference. |
| 7 | **Performance** | • Profile API latency; aim < 1 s.<br>• Optimize DB queries. | `backend/src/middleware/performance.js` | Use **pg-bench** for load testing. |

---

## Epic E3 – AR Coaching

| # | Task | Sub‑tasks | Expected Files / Modules | Implementation Notes |
|---|------|-----------|--------------------------|----------------------|
| 1 | **AR SDK Integration** | • Add **ARKit** (iOS) & **ARCore** (Android).<br>• Wrap in a cross‑platform component. | `src/mobile/components/ARCoach.{js,tsx}` | Use **react-native-arkit** / **react-native-arcore**. |
| 2 | **Pose‑Estimation Model** | • Deploy TensorFlow Lite model for real‑time pose detection.<br>• Expose `/ar/validate` endpoint. | `backend/src/services/arValidator.js` | Model runs on device; server verifies pose data for analytics. |
| 3 | **AR Coaching Flow** | • On exercise detail, tap “Start AR” → camera view with overlay.<br>• Show real‑time feedback (e.g., “Raise arm”). | `src/mobile/screens/ARCoachScreen.{js,tsx}` | Use **react-native-camera** + **TensorFlow Lite** inference. |
| 4 | **Server‑Side Pose Logging** | • POST `/ar/log` with pose frames & timestamps.<br>• Store in `ARLog` table. | `backend/src/routes/ar.js`, `backend/src/controllers/arController.js` | For later analytics & coach review. |
| 5 | **Unit & E2E Tests** | • Mock camera input.<br>• Verify overlay accuracy. | `src/mobile/__tests__/ARCoachScreen.test.js` | Use **Detox** + **jest-mock**. |
| 6 | **Performance** | • Ensure AR frame rate ≥ 30 fps.<br>• Optimize model quantization. | `backend/src/services/arValidator.js` | Use **TensorFlow Lite** quantized model. |

---

## Epic E4 – Progress & Analytics

| # | Task | Sub‑tasks | Expected Files / Modules | Implementation Notes |
|---|------|-----------|--------------------------|----------------------|
| 1 | **Progress Data Model** | • `WorkoutSession`, `ExerciseResult` tables.<br>• Store metrics (reps, weight, heart‑rate). | `backend/prisma/schema.prisma` | Use `DateTime` for timestamps. |
| 2 | **API Endpoints** | • `/progress/sessions` (GET/POST).<br>• `/progress/summary` (aggregate