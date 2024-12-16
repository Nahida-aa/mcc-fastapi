import type { CookieSerializeOptions } from "../../../node_modules/.pnpm/@types+cookie@0.6.0/node_modules/@types/cookie/index"

import { Cookie } from "./lib/utils/cookie"

export type Awaitable<T> = T | PromiseLike<T>

type ISODateString = string
export interface DefaultSession {
  user?: User
  expires: ISODateString
}
/** The active session of the logged in user. */
export interface Session extends DefaultSession {}

// 152
export interface Profile {
  id?: string | null
  sub?: string | null
  name?: string | null
  given_name?: string | null
  family_name?: string | null
  middle_name?: string | null
  nickname?: string | null
  preferred_username?: string | null
  profile?: string | null
  picture?: string | null | any
  website?: string | null
  email?: string | null
  email_verified?: boolean | null
  gender?: string | null
  birthdate?: string | null
  zoneinfo?: string | null
  locale?: string | null
  phone_number?: string | null
  updated_at?: Date | string | number | null
  address?: {
    formatted?: string | null
    street_address?: string | null
    locality?: string | null
    region?: string | null
    postal_code?: string | null
    country?: string | null
  } | null
  [claim: string]: unknown
}

// /** [Documentation](https://authjs.dev/reference/core#cookies) */ 183
export interface CookieOption {
  name: string
  options: CookieSerializeOptions
}
export type AuthAction =
  | "callback"
  | "csrf"
  | "error"
  | "providers"
  | "session"
  | "signin"
  | "signout"
  | "verify-request"
  | "webauthn-options"

  // /** @internal */ 330
export interface RequestInternal {
  url: URL
  method: "GET" | "POST"
  cookies?: Partial<Record<string, string>>
  headers?: Record<string, any>
  query?: Record<string, any>
  body?: Record<string, any>
  action: AuthAction
  providerId?: string
  error?: string
}

// Should only be used by frameworks 343
export interface ResponseInternal<
Body extends string | Record<string, any> | any[] | null = any,
> {
  status?: number
  headers?: Headers | HeadersInit
  body?: Body
  redirect?: string
  cookies?: Cookie[]
}