async function hashPassword(password: string): Promise<string> {
  // Convert password string to Uint8Array
  const encoder = new TextEncoder()
  const data = encoder.encode(password)

  // Calculate hash
  const hashBuffer = await crypto.subtle.digest('SHA-256', data)

  // Convert hash to hex string
  const hashArray = Array.from(new Uint8Array(hashBuffer))
  const hashHex = hashArray.map((b) => b.toString(16).padStart(2, '0')).join('')

  return hashHex
}

export { hashPassword }
