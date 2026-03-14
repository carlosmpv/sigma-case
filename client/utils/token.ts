import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'


export async function getAccessToken(): Promise<string | null> {
  const cookieStore = await cookies()
  const accessToken = await cookieStore.get('access_token')
  if (!accessToken?.value) {
    console.log('nao encontrado')
    redirect('/')
  }

  return accessToken!.value
}