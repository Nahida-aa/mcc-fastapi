// import { Profile } from "../types";
// // 29
// export type ProviderType =
//   | "oidc"
//   | "oauth"
//   | "email"
//   | "credentials"
//   | WebAuthnProviderType

// export type Provider<P extends Profile = any> = (
//   | ((
//       | OIDCConfig<P>
//       | OAuth2Config<P>
//       | EmailConfig
//       | CredentialsConfig
//       | WebAuthnConfig
//     ) &
//       InternalProviderOptions)
//   | ((
//       ...args: any
//     ) => (
//       | OAuth2Config<P>
//       | OIDCConfig<P>
//       | EmailConfig
//       | CredentialsConfig
//       | WebAuthnConfig
//     ) &
//       InternalProviderOptions)
// ) &
//   InternalProviderOptions