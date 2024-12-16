// "use server";
import { headers as nextHeaders } from "next/headers"
import { cookies } from 'next/headers'
import { AuthAction } from "./core/types";
// import { Auth, AuthConfig } from "./core";
// import { NextAuthConfig } from "./core/lib";
import { redirect } from "next/navigation";
import { raw, skipCSRFCheck } from "./core/lib/symbols";

export async function auth(){
  const cookieStore = cookies();
  const token = cookieStore.get('access_token');
  
  if (!token) {
    return null;
  }
  // 解密 token
  const user = JSON.parse(atob(token.value.split('.')[1]));
  return { user };
}

type SignInParams = [(string & {}) | undefined, 
  options?: FormData | ({
    redirectTo?: string;
    redirect?: boolean | undefined;
} & Record<string, any>) | undefined,
  authorizationParams?:
  | string[][]
  | Record<string, string>
  | string
  | URLSearchParams
]
// export async function signIn(
//   provider: SignInParams[0],
//   options: SignInParams[1] = {},
//   authorizationParams?: SignInParams[2],
//   config?: NextAuthConfig
// ){ 
//   console.log(`app/(auth)/actions.ts: signIn: provider: ${provider}`)
//   console.log(`app/(auth)/actions.ts: signIn: options: ${JSON.stringify(options)}`)
//   const headers = new Headers(await nextHeaders())
//   const {
//     redirect: shouldRedirect = true,
//     redirectTo,
//     ...rest
//   } = options instanceof FormData ? Object.fromEntries(options) : options

//   const callbackUrl = redirectTo?.toString() ?? headers.get("Referer") ?? "/"
//   console.log(`app/(auth)/actions.ts: signIn: callbackUrl: ${callbackUrl}`)

//   const signInURL = createActionURL(
//     "signin",
//     // @ts-expect-error `x-forwarded-proto` is not nullable, next.js sets it by default
//     headers.get("x-forwarded-proto"),
//     headers,
//     // process.env,
//     config
//   )
//   console.log(`app/(auth)/actions.ts: signIn: provider: ${provider}`)
//   console.log(`app/(auth)/actions.ts: signIn: authorizationParams: ${JSON.stringify(authorizationParams)}`)
//   let url = `${signInURL}/${provider}?${new URLSearchParams(
//     authorizationParams
//   )}`
//   console.log(`app/(auth)/actions.ts: signIn: url: ${url}`)

//   headers.set("Content-Type", "application/x-www-form-urlencoded")
//   const body = new URLSearchParams({ ...rest, callbackUrl })
//   const req = new Request(url, { method: "POST", headers, body })

//   const res = await Auth(req, { ...config, raw, skipCSRFCheck })


//   const cookieStore = cookies();
//   for (const c of res?.cookies ?? []) cookieStore.set(c.name, c.value, c.options)

//   const responseUrl = res instanceof Response ? res.headers.get("Location") : res.redirect

//   // NOTE: if for some unexpected reason the responseUrl is not set,
//   // we redirect to the original url
//   const redirectUrl = responseUrl ?? url
  
//   if (shouldRedirect) return redirect(redirectUrl)

//   return redirectUrl as any
//   // const response = await fetch('/api/py/sign-in', {
//   //   method: 'POST',
//   //   headers: { 'Content-Type': 'application/json' },
//   //   body: JSON.stringify({ username: 'admin', password: 'admin' }),
//   // });

//   // if (response.ok) {
//   //   const { access_token, refresh_token } = await response.json();
//   //   const cookieStore = cookies();
//   //   cookieStore.set('access_token', access_token, { maxAge: 60 * 60 }); // 1 hour
//   //   cookieStore.set('refresh_token', refresh_token, { maxAge: 60 * 60 * 24 * 7 }); // 1 week
//   // }
// }

type SignOutParams = [options?: { 
  redirectTo?: string; 
  // The relative path to redirect to after signing out. By default, the user is redirected to the current page.
  // 登出后重定向的相对路径。默认情况下，用户将被重定向到当前页面。
  redirect?: boolean|undefined 
  // If set to `false`, the `signOut` method will return the URL to redirect to instead of redirecting automatically. 
  // 如果设置为 `false`，`signOut` 方法将返回要重定向到的 URL，而不是自动重定向。
  }|undefined
];
// export const signOut = async <R extends boolean = true>(options: SignOutParams[0] = {
// }): Promise<R extends false ? any : never> => {
//   const headers = new Headers(await nextHeaders())

//   headers.set("Content-Type", "application/x-www-form-urlencoded")
//   const url = createActionURL(
//     "signout",
//     // @ts-expect-error `x-forwarded-proto` is not nullable, next.js sets it by default
//     headers.get("x-forwarded-proto"),
//     headers,
//     // process.env,
//     // config
//   )
//   const callbackUrl = options?.redirectTo ?? headers.get("Referer") ?? "/"
//   const body = new URLSearchParams({ callbackUrl })
//   const req = new Request(url, { method: "POST", headers, body })
//   const res = await Auth(req, { 
//     // ...config, 
//     raw, skipCSRFCheck })

//   const cookieStore = cookies();
//   for (const c of res?.cookies ?? []) cookieStore.set(c.name, c.value, c.options)

//   if (options?.redirect ?? true) return redirect(res.redirect!)
//   return res as any
// }


// export function createActionURL(
//   action: AuthAction,
//   protocol: string,
//   headers: Headers,
//   // envObject: any,
//   config: Pick<AuthConfig, "basePath" | "logger">
// ): URL {
//   const basePath = config?.basePath ?? "api/auth"

//   const detectedHost = headers.get("x-forwarded-host") ?? headers.get("host")
//   const detectedProtocol =
//     headers.get("x-forwarded-proto") ?? protocol ?? "https"
//   const _protocol = detectedProtocol.endsWith(":")
//     ? detectedProtocol
//     : detectedProtocol + ":"

//   let url = new URL(`${_protocol}//${detectedHost}`)
//   const sanitizedUrl = url.toString().replace(/\/$/, "")

//   if (basePath) {
//     // remove leading and trailing slash
//     const sanitizedBasePath = basePath?.replace(/(^\/|\/$)/g, "") ?? ""
//     return new URL(`${sanitizedUrl}/${sanitizedBasePath}/${action}`)
//   }
//   return new URL(`${sanitizedUrl}/${action}`)
// }