// "use server";
import { cookies } from 'next/headers'
// import { redirect } from "next/navigation";

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

export interface AuthConfig {
  /**
   * The base path of the Auth.js API endpoints.
   *
   * @default "/api/auth" in "next-auth"; "/auth" with all other frameworks
   */
  basePath?: string
}
export function createActionURL(
  action: string,
  protocol: string,
  headers: Headers,
  // envObject: any,
  config: Pick<AuthConfig, "basePath">
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