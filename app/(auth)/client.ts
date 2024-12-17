"use client"

import { AuthError } from "next-auth"
import { LoggerInstance } from "./core/lib/utils/logger"
import { Session } from "./core/types"
import { redirect } from "next/dist/server/api-utils"

/** @todo */
class ClientFetchError extends AuthError {} // lib/client.ts: 9

export interface AuthClientConfig { // lib/client.ts: 14
  baseUrl: string
  basePath: string
  baseUrlServer: string
  basePathServer: string
  /** Stores last session response */
  _session?: Session | null | undefined
  /** Used for timestamp since last sycned (in seconds) */
  _lastSync: number
  /**
   * Stores the `SessionProvider`'s session update method to be able to
   * trigger session updates from places like `signIn` or `signOut`
   */
  _getSession: (...args: any[]) => any
}

/** [Documentation](https://next-auth.js.org/getting-started/client#using-the-redirect-false-option-1) */
export interface SignOutResponse { // lib/client.ts: 89
  url: string
}
export interface SignOutParams<R extends boolean = true> { // lib/client.ts: 93
  /** @deprecated Use `redirectTo` instead.
   */
  callbackUrl?: string // 这是一个已弃用的参数，建议使用 redirectTo 代替。它指定用户退出登录后重定向的 URL

  /**
   * If you pass `redirect: false`, the page will not reload.
   * The session will be deleted, and `useSession` is notified, so any indication about the user will be shown as logged out automatically.
   * It can give a very nice experience for the user.
   */
  redirectTo?: string
  /** [Documentation](https://next-auth.js.org/getting-started/client#using-the-redirect-false-option-1 */
  redirect?: R
}

/**
 * If passed 'appContext' via getInitialProps() in _app.js
 * then get the req object from ctx and use that for the
 * req value to allow `fetchData` to
 * work seemlessly in getInitialProps() on server side
 * pages *and* in _app.js.
 * @internal
 */
export async function fetchData<T = any>( // lib/client.ts: 147
  path: string,
  __NEXTAUTH: AuthClientConfig,
  logger: LoggerInstance,
  req: any = {}
): Promise<T | null> {
  const url = `${apiBaseUrl(__NEXTAUTH)}/${path}`
  try {
    const options: RequestInit = {
      headers: {
        "Content-Type": "application/json",
        ...(req?.headers?.cookie ? { cookie: req.headers.cookie } : {}),
      },
    }

    if (req?.body) {
      options.body = JSON.stringify(req.body)
      options.method = "POST"
    }

    const res = await fetch(url, options)
    const data = await res.json()
    if (!res.ok) throw data
    return data
  } catch (error) {
    logger.error(new ClientFetchError((error as Error).message, error as any))
    return null
  }
}

/** @internal */
export function apiBaseUrl(__NEXTAUTH: AuthClientConfig) { // lib/client.ts: 177
  if (typeof window === "undefined") {
    // Return absolute path when called server side
    console.log(`__NEXTAUTH.baseUrlServer: ${__NEXTAUTH.baseUrlServer}`)
    console.log(`__NEXTAUTH.basePathServer: ${__NEXTAUTH.basePathServer}`)
    return `${__NEXTAUTH.baseUrlServer}${__NEXTAUTH.basePathServer}`
  }
  // Return relative path when called client side
  console.log(`__NEXTAUTH.basePath: ${__NEXTAUTH.basePath}`)
  return __NEXTAUTH.basePath
}

export function parseUrl(url?: string): { // lib/client.ts: 221
  /** @default "http://localhost:3000" */
  origin: string
  /** @default "localhost:3000" */
  host: string
  /** @default "/api/auth" */
  path: string
  /** @default "http://localhost:3000/api/auth" */
  base: string
  /** @default "http://localhost:3000/api/auth" */
  toString: () => string
} {
  const defaultUrl = new URL("http://localhost:3000/api/auth")

  if (url && !url.startsWith("http")) {
    url = `https://${url}`
  }
  console.log(`parseUrl::url: ${url}`)
  const _url = new URL(url || defaultUrl)
  const path = (_url.pathname === "/" ? defaultUrl.pathname : _url.pathname)
    // Remove trailing slash
    .replace(/\/$/, "")

  console.log(`parseUrl::path: ${path}`)
  const base = `${_url.origin}${path}`
  return {
    origin: _url.origin,
    host: _url.host,
    path,
    base,
    toString: () => base,
  }
}
export const __NEXTAUTH: AuthClientConfig = { // 59
  baseUrl: parseUrl(process.env.NEXTAUTH_URL ?? process.env.VERCEL_URL).origin,
  basePath: parseUrl(process.env.NEXTAUTH_URL).path, // 客户端不到 env, 从而客户端拿到 默认值
  baseUrlServer: parseUrl(
    process.env.NEXTAUTH_URL_INTERNAL ??
      process.env.NEXTAUTH_URL ??
      process.env.VERCEL_URL
  ).origin,
  basePathServer: parseUrl(
    process.env.NEXTAUTH_URL_INTERNAL ?? process.env.NEXTAUTH_URL
  ).path,
  _lastSync: 0,
  _session: undefined,
  _getSession: () => {},
}

let broadcastChannel: BroadcastChannel | null = null // 75

function getNewBroadcastChannel() { // 77
  return new BroadcastChannel("next-auth")
}

function broadcast() { // 81
  if (typeof BroadcastChannel === "undefined") {
    return {
      postMessage: () => {},
      addEventListener: () => {},
      removeEventListener: () => {},
    }
  }

  if (broadcastChannel === null) {
    broadcastChannel = getNewBroadcastChannel()
  }

  return broadcastChannel
}

// TODO:
const logger: LoggerInstance = { // 98
  debug: console.debug,
  error: console.error,
  warn: console.warn,
}

/**
 * Returns the current Cross-Site Request Forgery Token (CSRF Token)
 * required to make requests that changes state. (e.g. signing in or out, or updating the session).
 *
 * [CSRF Prevention: Double Submit Cookie](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#double-submit-cookie)
 */
export async function getCsrfToken() {
  const response = await fetchData<{ csrfToken: string }>( // 203
    "csrf",
    __NEXTAUTH,
    logger
  )
  return response?.csrfToken ?? ""
}

export async function signOut<R extends boolean = true>( // 318
  options?: SignOutParams<R>
): Promise<R extends true ? undefined : SignOutResponse> {
  const redirectTo =
    options?.redirectTo ?? options?.callbackUrl ?? window.location.href
  console.log(`signOut::redirectTo: ${redirectTo}`)
  const baseUrl = apiBaseUrl(__NEXTAUTH)
  const csrfToken = await getCsrfToken()
  console.log(`signOut::csrfToken: ${csrfToken}`)
  const res = await fetch(`${baseUrl}/signout`, {
    method: "post",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-Auth-Return-Redirect": "1",
    },
    body: new URLSearchParams({ csrfToken, callbackUrl: redirectTo }),
  })
  const data = await res.json() // { url: redirectTo }

  broadcast().postMessage({ event: "session", data: { trigger: "signout" } })

  if (options?.redirect ?? true) {
    const url = data.url ?? redirectTo
    window.location.href = url
    // If url contains a hash, the browser does not reload the page. We reload manually
    if (url.includes("#")) window.location.reload()
    // @ts-expect-error
    return
  }

  await __NEXTAUTH._getSession({ event: "storage" })

  return data
}

interface ClientSignOutOptionsI<R extends boolean = true> {
  redirectTo?: string
  redirect?: R
} // ts 中没有下面python的写法, 但是可以通过 interface 来实现
// class PyModel():
//   redirectTo: string|None = None
//   redirect: bool = True
type ClientSignOutOptions = {
  redirectTo?: string
  redirect?: boolean
}
/**
 * Signs the user out.
 * 
 * @param options - Options for signing out.
 * @param options.redirectTo - URL to redirect to after sign out. Defaults to "/".
 * @param options.redirect - Whether to redirect after sign out. Defaults to true.
 * @returns A promise that resolves to undefined if redirect is true, or to a SignOutResponse if redirect is false.
 */
export async function client_sign_out( 
    options
    :  { redirectTo?: string
      redirect?: boolean }={ redirect: true}
) {
  const redirectTo = options.redirectTo ?? window.location.href // 没有设置 redirectTo 时默认为当前页面
  const baseUrl = "/api/py/auth"
  const csrfToken = await getPyCsrfToken()
  console.log(`signOut::csrfToken: ${csrfToken}`)
  const res = await fetch(`${baseUrl}/signout`, {
    method: "post",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-Auth-Return-Redirect": "1",
    },
    body: new URLSearchParams({ csrfToken, redirectTo: redirectTo }),
  })
  if (!res.ok) {
    throw new Error("Failed to sign out")
  }
  const data = await res.json() // { url: redirectTo }
  console.log(`signOut::data: ${data}`)
  broadcast().postMessage({ event: "session", data: { trigger: "signout" } })
  if (options?.redirect ?? true) {
    const url = data.url ?? redirectTo
    window.location.href = url
    // If url contains a hash, the browser does not reload the page. We reload manually
    if (url.includes("#")) window.location.reload()
    //  "at" ts-expect-error
    return
  }
  return data
  // return signOut(options)
}
export async function getPyCsrfToken() {
  const res = await fetch("/api/py/auth/csrf")
  const data = await res.json()
  return data?.csrfToken ?? ""
}