// "use server";
import { headers as nextHeaders } from "next/headers"
import { cookies } from 'next/headers'
import { AuthAction } from "./core/types";
import { 
  // Auth, 
  AuthConfig } from "./core";
import { NextAuthConfig } from "./core/lib";
// import { redirect } from "next/navigation";
import { raw, skipCSRFCheck } from "./core/lib/symbols";

export async function server_auth(){
  const cookieStore = cookies();
  const token = cookieStore.get('access_token');
  
  if (!token) {
    return null;
  }
  // 解密 token
  const payload = token.value.split('.')[1];
  const base64 = payload.replace(/-/g, '+').replace(/_/g, '/'); // 将 Base64 URL 安全编码转换为标准 Base64 编码
  const padding = '='.repeat((4 - (payload.length % 4)) % 4);
  const decodedPayload = atob(base64 + padding);
  const user = JSON.parse(decodedPayload);
  return { user:
    { id: user.id, name: user.name, email: user.email, image: user.image, nickname: user.nickname }
   };
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
export async function signIn(
  provider: SignInParams[0],
  options: SignInParams[1] = {},
  authorizationParams?: SignInParams[2],
  config?: NextAuthConfig
){ 
  console.log(`app/(auth)/actions.ts: signIn: provider: ${provider}`)
  console.log(`app/(auth)/actions.ts: signIn: options: ${JSON.stringify(options)}`)
  const headers = new Headers(await nextHeaders())
  const {
    redirect: shouldRedirect = true,
    redirectTo,
    ...rest
  } = options instanceof FormData ? Object.fromEntries(options) : options
  console.log(`app/(auth)/actions.ts: signIn: shouldRedirect: ${shouldRedirect}`)

  const callbackUrl = redirectTo?.toString() ?? headers.get("Referer") ?? "/"
  console.log(`app/(auth)/actions.ts: signIn: rest: ${JSON.stringify(rest)}`)

  const signInURL = createActionURL(
    "signin",
    // @ts-expect-error `x-forwarded-proto` is not nullable, next.js sets it by default
    headers.get("x-forwarded-proto"),
    headers,
    // process.env,
    config
  )
  console.log(`app/(auth)/actions.ts: signIn: authorizationParams: ${JSON.stringify(authorizationParams)}`)
  let url = `${signInURL}`
  if (provider == "py"){
    url = `${signInURL}?${new URLSearchParams(
      authorizationParams
    )}`
  } else{
    url = `${signInURL}/${provider}?${new URLSearchParams(
      authorizationParams
    )}`
  }
  console.log(`app/(auth)/actions.ts: signIn: url: ${url}`)

  headers.set("Content-Type", "application/x-www-form-urlencoded")
  console.log(`app/(auth)/actions.ts: signIn: headers: ${JSON.stringify([...headers])}`)
  const body = new URLSearchParams({ ...rest, callbackUrl })
  console.log(`app/(auth)/actions.ts: signIn: body: ${body.toString()}`)
  // const req = new Request(url, { method: "POST", headers, body })
  // console.log(`app/(auth)/actions.ts: signIn: req method: ${req.method}`);
  // console.log(`app/(auth)/actions.ts: signIn: req url: ${req.url}`);
  // console.log(`app/(auth)/actions.ts: signIn: req headers: ${JSON.stringify([...req.headers])}`);
  // console.log(`app/(auth)/actions.ts: signIn: req body: ${await req.text()}`);

  // const res = await Auth(req, { ...config, raw, skipCSRFCheck })
  try {
    const res = await fetch(url,
      {
        method: "POST",
        headers: headers,
        body: body,
      }
    );
    // console.log(`app/(auth)/actions.ts: signIn: response status: ${res.status}`);
    if (res.ok) {
      const data = await res.json();
      console.log(`app/(auth)/actions.ts: signIn: data: ${JSON.stringify(data)}`);
    } else {
      console.error(`app/(auth)/actions.ts: signIn: error: ${res.statusText}`);
    }
  } catch (error) {
    console.error(`app/(auth)/actions.ts: signIn: error: ${error}`)
  }

  // const cookieStore = cookies();
  // for (const c of res?.cookies ?? []) cookieStore.set(c.name, c.value, c.options)

  // const responseUrl = res instanceof Response ? res.headers.get("Location") : res.redirect

  // NOTE: if for some unexpected reason the responseUrl is not set,
  // we redirect to the original url
  // const redirectUrl = responseUrl ?? url
  
  // if (shouldRedirect) return redirect(redirectUrl)

  // return redirectUrl as any
  // const response = await fetch('/api/py/sign-in', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ username: 'admin', password: 'admin' }),
  // });


  // }
}

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


export function createActionURL(
  action: AuthAction,
  protocol: string,
  headers: Headers,
  // envObject: any,
  config: Pick<AuthConfig, "basePath" | "logger">
): URL {
  const basePath = config?.basePath ?? "api/auth"

  const detectedHost = headers.get("x-forwarded-host") ?? headers.get("host")
  const detectedProtocol = headers.get("x-forwarded-proto") ?? protocol ?? "https"
  const _protocol = detectedProtocol.endsWith(":")
    ? detectedProtocol
    : detectedProtocol + ":"

  let url = new URL(`${_protocol}//${detectedHost}`)
  const sanitizedUrl = url.toString().replace(/\/$/, "")

  if (basePath) {
    // remove leading and trailing slash
    const sanitizedBasePath = basePath?.replace(/(^\/|\/$)/g, "") ?? ""
    return new URL(`${sanitizedUrl}/${sanitizedBasePath}/${action}`)
  }
  return new URL(`${sanitizedUrl}/${action}`)
}