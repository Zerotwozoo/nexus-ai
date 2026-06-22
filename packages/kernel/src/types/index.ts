export type UUID = string;
export type ISO8601 = string;
export type Email = string;
export type URLString = string;
export type JSONValue = string | number | boolean | null | JSONValue[] | { [key: string]: JSONValue };
export type JSONObject = { [key: string]: JSONValue };

export type Timestamps = {
  created_at: ISO8601;
  updated_at: ISO8601;
};

export type PaginationParams = {
  page?: number;
  per_page?: number;
  sort_by?: string;
  sort_order?: "asc" | "desc";
};

export type PaginatedResponse<T> = {
  data: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
  has_next: boolean;
  has_previous: boolean;
};

export type ApiResponse<T> = {
  success: boolean;
  data?: T;
  error?: ApiError;
  meta?: Record<string, unknown>;
};

export type ApiError = {
  code: string;
  message: string;
  details?: Record<string, string[]>;
};

export enum UserRole {
  OWNER = "owner",
  ADMIN = "admin",
  MEMBER = "member",
  VIEWER = "viewer",
}

export enum WorkspacePlan {
  FREE = "free",
  PRO = "pro",
  BUSINESS = "business",
  ENTERPRISE = "enterprise",
}

export enum TaskStatus {
  BACKLOG = "backlog",
  TODO = "todo",
  IN_PROGRESS = "in_progress",
  REVIEW = "review",
  DONE = "done",
}

export enum Priority {
  URGENT = "urgent",
  HIGH = "high",
  MEDIUM = "medium",
  LOW = "low",
}

export enum AIModel {
  GPT4O = "gpt-4o",
  GPT4O_MINI = "gpt-4o-mini",
  CLAUDE_SONNET = "claude-sonnet-4",
  CLAUDE_HAIKU = "claude-haiku-3",
  GROQ_LLAMA = "groq-llama-3",
  CUSTOM = "custom",
}
