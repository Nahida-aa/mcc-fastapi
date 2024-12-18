"use client"

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
  // broadcast().postMessage({ event: "session", data: { trigger: "signout" } })
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