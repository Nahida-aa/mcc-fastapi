export type WarningCode = // 4
  | "debug-enabled"
  | "csrf-disabled"
  | "experimental-webauthn"
  | "env-url-basepath-redundant"
  | "env-url-basepath-mismatch"


export interface LoggerInstance extends Record<string, Function> { // 17
  warn: (code: WarningCode) => void
  error: (error: Error) => void
  debug: (message: string, metadata?: unknown) => void
}