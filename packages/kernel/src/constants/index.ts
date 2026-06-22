export const PAGINATION = {
  DEFAULT_PAGE: 1,
  DEFAULT_PER_PAGE: 20,
  MAX_PER_PAGE: 100,
} as const;

export const RATE_LIMITS = {
  DEFAULT: 60,
  AUTH: 10,
  AI: 30,
  EXPORT: 5,
} as const;

export const FILE_LIMITS = {
  MAX_UPLOAD_SIZE: 50 * 1024 * 1024, // 50MB
  MAX_AVATAR_SIZE: 5 * 1024 * 1024, // 5MB
  ALLOWED_IMAGE_TYPES: ["image/jpeg", "image/png", "image/webp", "image/gif"],
  ALLOWED_DOCUMENT_TYPES: [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/plain",
    "text/markdown",
  ],
} as const;

export const AI = {
  MAX_TOKENS: 4096,
  DEFAULT_TEMPERATURE: 0.7,
  MEMORY_LIMIT: 50,
  MAX_CONVERSATION_HISTORY: 100,
  EMBEDDING_MODEL: "text-embedding-3-small",
  EMBEDDING_DIMENSION: 1536,
} as const;

export const AUTH = {
  ACCESS_TOKEN_EXPIRE_MINUTES: 15,
  REFRESH_TOKEN_EXPIRE_DAYS: 7,
  PASSWORD_MIN_LENGTH: 8,
  PASSWORD_MAX_LENGTH: 128,
  VERIFICATION_CODE_EXPIRE_MINUTES: 10,
  MAX_LOGIN_ATTEMPTS: 5,
  LOCKOUT_DURATION_MINUTES: 15,
} as const;

export const WORKSPACE = {
  MAX_MEMBERS_FREE: 3,
  MAX_MEMBERS_PRO: 15,
  MAX_MEMBERS_BUSINESS: 50,
  MAX_STORAGE_FREE: 500 * 1024 * 1024, // 500MB
  MAX_STORAGE_PRO: 10 * 1024 * 1024 * 1024, // 10GB
  MAX_STORAGE_BUSINESS: 100 * 1024 * 1024 * 1024, // 100GB
} as const;
