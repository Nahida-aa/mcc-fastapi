// import { NextRequest, NextResponse } from "next/server"
// import { AuthConfig } from ".."
// import { Awaitable, RequestInternal, ResponseInternal, Session } from "../types"
// import { skipCSRFCheck } from "./symbols"
// import * as actions from "./actions"

// /** @internal */
// export async function AuthInternal( // 14
//   request: RequestInternal,
//   authOptions: AuthConfig
// ): Promise<ResponseInternal> {
//   const { action, providerId, error, method } = request

//   const csrfDisabled = authOptions.skipCSRFCheck === skipCSRFCheck

//   const { options, cookies } = await init({ // 初始化配置和 cookies
//     authOptions,
//     action,
//     providerId,
//     url: request.url,
//     callbackUrl: request.body?.callbackUrl ?? request.query?.callbackUrl,
//     csrfToken: request.body?.csrfToken,
//     cookies: request.cookies,
//     isPost: method === "POST",
//     csrfDisabled,
//   })

//   const sessionStore = new SessionStore( // 创建 SessionStore 实例来管理会话
//     options.cookies.sessionToken,
//     request.cookies,
//     options.logger
//   )

//   if (method === "GET") {
//     const render = renderPage({ ...options, query: request.query, cookies })
//     switch (action) {
//       case "callback":
//         return await actions.callback(request, options, sessionStore, cookies)
//       case "csrf":
//         return render.csrf(csrfDisabled, options, cookies)
//       case "error":
//         return render.error(error)
//       case "providers":
//         return render.providers(options.providers)
//       case "session":
//         return await actions.session(options, sessionStore, cookies)
//       case "signin":
//         return render.signin(providerId, error)
//       case "signout":
//         return render.signout()
//       case "verify-request":
//         return render.verifyRequest()
//       case "webauthn-options":
//         return await actions.webAuthnOptions(
//           request,
//           options,
//           sessionStore,
//           cookies
//         )
//       default:
//     }
//   } else { // POST 请求处理：验证 CSRF 令牌后，根据不同的操作类型调用相应的处理函数
//     const { csrfTokenVerified } = options
//     switch (action) {
//       case "callback":
//         if (options.provider.type === "credentials")
//           // Verified CSRF Token required for credentials providers only
//           validateCSRF(action, csrfTokenVerified)
//         return await actions.callback(request, options, sessionStore, cookies)
//       case "session":
//         validateCSRF(action, csrfTokenVerified)
//         return await actions.session(
//           options,
//           sessionStore,
//           cookies,
//           true,
//           request.body?.data
//         )
//       case "signin":
//         validateCSRF(action, csrfTokenVerified)
//         return await actions.signIn(request, cookies, options)

//       case "signout":
//         validateCSRF(action, csrfTokenVerified)
//         return await actions.signOut(cookies, sessionStore, options)
//       default:
//     }
//   }
//   throw new UnknownAction(`Cannot handle action: ${action}`)
// }

// /** Configure NextAuth.js. */
// export interface NextAuthConfig extends Omit<AuthConfig, "raw"> {
//   /**
//    * Callbacks are asynchronous functions you can use to control what happens when an auth-related action is performed.
//    * Callbacks **allow you to implement access controls without a database** or to **integrate with external databases or APIs**.
//    */
//   // callbacks?: AuthConfig["callbacks"] & {
//   //   /**
//   //    * Invoked when a user needs authorization, using [Middleware](https://nextjs.org/docs/advanced-features/middleware).
//   //    *
//   //    * You can override this behavior by returning a {@link NextResponse}.
//   //    *
//   //    * @example
//   //    * ```ts title="app/auth.ts"
//   //    * async authorized({ request, auth }) {
//   //    *   const url = request.nextUrl
//   //    *
//   //    *   if(request.method === "POST") {
//   //    *     const { authToken } = (await request.json()) ?? {}
//   //    *     // If the request has a valid auth token, it is authorized
//   //    *     const valid = await validateAuthToken(authToken)
//   //    *     if(valid) return true
//   //    *     return NextResponse.json("Invalid auth token", { status: 401 })
//   //    *   }
//   //    *
//   //    *   // Logged in users are authenticated, otherwise redirect to login page
//   //    *   return !!auth.user
//   //    * }
//   //    * ```
//   //    *
//   //    * :::warning
//   //    * If you are returning a redirect response, make sure that the page you are redirecting to is not protected by this callback,
//   //    * otherwise you could end up in an infinite redirect loop.
//   //    * :::
//   //    */
//   //   authorized?: (params: {
//   //     /** The request to be authorized. */
//   //     request: NextRequest
//   //     /** The authenticated user or token, if any. */
//   //     auth: Session | null
//   //   }) => Awaitable<boolean | NextResponse | Response | undefined>
//   // }
// }