// import { RequestInternal, ResponseInternal } from "../../../types"
// import { Cookie } from "../../utils/cookie"

// export async function signIn( // 11
//   request: RequestInternal,
//   cookies: Cookie[],
//   options: InternalOptions
// ): Promise<ResponseInternal> {
//   const signInUrl = `${options.url.origin}${options.basePath}/signin`

//   if (!options.provider) return { redirect: signInUrl, cookies }

//   switch (options.provider.type) {
//     case "oauth":
//     case "oidc": {
//       const { redirect, cookies: authCookies } = await getAuthorizationUrl(
//         request.query,
//         options
//       )
//       if (authCookies) cookies.push(...authCookies)
//       return { redirect, cookies }
//     }
//     case "email": {
//       const response = await sendToken(request, options)
//       return { ...response, cookies }
//     }
//     default:
//       return { redirect: signInUrl, cookies }
//   }
// }