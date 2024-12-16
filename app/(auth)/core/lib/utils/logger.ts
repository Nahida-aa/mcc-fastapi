export type WarningCode = // 4
  | "debug-enabled"
  | "csrf-disabled"
  | "experimental-webauthn"
  | "env-url-basepath-redundant"
  | "env-url-basepath-mismatch"


/**
 * Override any of the methods, and the rest will use the default logger.
 *
 * [Documentation](https://authjs.dev/reference/core#authconfig#logger)
 */
// eslint-disable-next-line @typescript-eslint/no-unsafe-function-type
export interface LoggerInstance extends Record<string, Function> { // 17
  warn: (code: WarningCode) => void
  error: (error: Error) => void
  debug: (message: string, metadata?: unknown) => void
}