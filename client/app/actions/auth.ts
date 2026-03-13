'use server'

import { cookies } from "next/headers"

export async function signin(prevstate: any, formData: FormData) {
    const response = await fetch(`${process.env.API_URL}/authenticate`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: (new URLSearchParams({
            "grant_type": "password",
            "username": formData.get('email')?.toString() || '',
            "password": formData.get('senha')?.toString() || '',
            "scope": "",
        })).toString()
    })

    if (!response.ok) {
        const { detail } = await response.json()
        return { 
            error: detail || '',
            success: false,
        }
    }

    const { access_token, token_type } = await response.json()

    const cookieStore = await cookies();
    cookieStore.set({
        name: 'access_token',
        value: access_token,
        httpOnly: true,
        sameSite: 'lax',
        path: '/',
    })

    return { error: '', success: true }
}

export async function signup(prevstate: any, formData: FormData) {
    /**
     * Por enquanto só usuario e senha mas ja da pra entender
     */

    const response = await fetch(`${process.env.API_URL}/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "username": formData.get('email'),
            "password": formData.get('senha')
        })
    })

    if (!response.ok) {
        const { detail } = await response.json()
        return {
            error: detail || '',
            success: false,
        }
    }

    return await signin(prevstate, formData);// se sucesso já loga
}